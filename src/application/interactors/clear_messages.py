import contextlib
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from infrastructure.cleaner import FoodMenuCleanerQueue


@dataclass(frozen=True, slots=True, kw_only=True)
class ClearMessagesInteractor:
    bot: Bot
    food_menu_cleaner_queue: FoodMenuCleanerQueue

    async def execute(self) -> None:
        chat_ids_and_message_ids = await self.food_menu_cleaner_queue.pop_all()

        for chat_id, message_ids in chat_ids_and_message_ids:
            with contextlib.suppress(TelegramAPIError):
                await self.bot.delete_messages(
                    chat_id=chat_id,
                    message_ids=list(message_ids),
                )
