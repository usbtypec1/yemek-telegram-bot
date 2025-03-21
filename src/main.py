import asyncio

import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import load_config_from_toml_file
from presentation.middlewares.access import AccessMiddleware
from presentation.telegram_handlers.food_menu import router
from infrastructure.cache import FoodMenuCache
from infrastructure.cleaner import FoodMenuCleanerQueue
from presentation.periodic_tasks.clear_messages import clear_messages
from presentation.periodic_tasks.prefetch_food_menu import prefetch_food_menu


async def main() -> None:
    config = load_config_from_toml_file()

    redis_client = redis.from_url(config.redis_url)
    food_menu_cache = FoodMenuCache(
        redis_client=redis_client,
        ttl_in_seconds=config.food_menu_ttl_in_seconds,
    )
    food_menu_cleaner_queue = FoodMenuCleanerQueue(redis_client=redis_client)

    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=clear_messages,
        trigger=CronTrigger(minute="*/5"),
        args=(bot, food_menu_cleaner_queue),
    )
    scheduler.add_job(
        func=prefetch_food_menu,
        trigger=CronTrigger(minute="*/5"),
        args=(food_menu_cache,),
    )
    scheduler.start()

    dispatcher = Dispatcher()
    dispatcher["food_menu_cache"] = food_menu_cache
    dispatcher["food_menu_cleaner_queue"] = food_menu_cleaner_queue

    dispatcher.update.middleware(
        AccessMiddleware(
            chat_id=config.access_chat_id,
            access_denied_text=config.access_denied_text,
        ),
    )

    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
