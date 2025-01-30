from aiogram import Bot

from infrastructure.cleaner import FoodMenuCleanerQueue
from application.interactors.clear_messages import ClearMessagesInteractor


async def clear_messages(
    bot: Bot, food_menu_cleaner_queue: FoodMenuCleanerQueue
):
    await ClearMessagesInteractor(
        bot=bot,
        food_menu_cleaner_queue=food_menu_cleaner_queue,
    ).execute()
