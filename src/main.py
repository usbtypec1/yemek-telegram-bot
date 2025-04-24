import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dishka.integrations.aiogram import setup_dishka
from dishka import make_async_container

from bootstrap.ioc.registry import get_providers
from presentation.middlewares.group_chat_warning import (
    group_chat_warning_middleware,
)
import presentation.telegram_handlers
from bootstrap.config.settings import Settings
from presentation.middlewares.access import AccessMiddleware
from presentation.periodic_tasks.prefetch_food_menu import prefetch_food_menu


async def main() -> None:
    settings = Settings.from_toml()

    container = make_async_container(
        *get_providers(),
        context={Settings: settings},
    )

    bot = Bot(
        token=settings.telegram_bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=prefetch_food_menu,
        trigger=CronTrigger(minute="*/5"),
        args=(container,)
    )
    scheduler.start()

    dispatcher = Dispatcher()
    dispatcher["bot_user"] = await bot.get_me()

    setup_dishka(container=container, router=dispatcher, auto_inject=True)

    dispatcher.update.outer_middleware(group_chat_warning_middleware)
    dispatcher.update.middleware(
        AccessMiddleware(
            chat_id=settings.access.chat_id,
            access_denied_text=settings.access.denied_text,
        ),
    )

    dispatcher.include_routers(
        presentation.telegram_handlers.help.router,
        presentation.telegram_handlers.food_menu.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
