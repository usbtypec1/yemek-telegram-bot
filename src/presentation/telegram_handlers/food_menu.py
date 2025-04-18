import sqlite3
from aiogram import Router, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from infrastructure.usage_statistics import UsageStatisticsDao
from presentation.ui.views.base import answer_media_group_view, answer_view
from presentation.ui.views.food_menu import (
    DailyFoodMenuView,
    UserPrivateChatMenuView,
)
from application.interactors.food_menu_fetch import (
    FoodMenuFetchInteractor,
)
from application.interactors.food_menu_for_specific_day import (
    FoodMenuForSpecificDayPickInteractor,
)
from application.interactors.track_usage import TrackUsageInteractor
from infrastructure.cache import FoodMenuCache
from infrastructure.cleaner import FoodMenuCleanerQueue


router = Router(name=__name__)


@router.message(
    F.text.in_(("🕕 Сегодня", "🕒 Завтра", "🕞 Послезавтра")),
)
async def on_show_food_menu_for_specific_day(
    message: Message,
    food_menu_cache: FoodMenuCache,
    food_menu_cleaner_queue: FoodMenuCleanerQueue,
):
    word_to_days_count = {
        "🕕 Сегодня": 0,
        "🕒 Завтра": 1,
        "🕞 Послезавтра": 2,
    }
    days_to_skip: int = word_to_days_count[message.text]  # type: ignore
    food_menu_fetch_interactor = FoodMenuFetchInteractor(cache=food_menu_cache)
    daily_food_menu_list = await food_menu_fetch_interactor.execute()

    food_menu_for_specific_day_pick_interactor = (
        FoodMenuForSpecificDayPickInteractor(
            daily_food_menu_list=daily_food_menu_list,
            days_to_skip=days_to_skip,
        )
    )
    daily_food_menu = food_menu_for_specific_day_pick_interactor.execute()

    if daily_food_menu is None:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyFoodMenuView(daily_food_menu)
    await answer_media_group_view(message, view)


@router.message(
    Command("yemek"),
    StateFilter("*"),
)
async def on_show_food_menu_for_specific_day_by_command(
    message: Message,
    food_menu_cache: FoodMenuCache,
    command: CommandObject,
):
    user_id = message.from_user.id  # type: ignore
    chat_id = message.chat.id  # type: ignore

    if not command.args:
        view = UserPrivateChatMenuView()
        await answer_view(message, view)
        return

    word_to_days_count = {
        "today": 0,
        "tomorrow": 1,
    }

    if command.args not in word_to_days_count:
        await message.reply("Не могу распознать день 😔")
        return

    days_to_skip = word_to_days_count[command.args]

    food_menu_fetch_interactor = FoodMenuFetchInteractor(cache=food_menu_cache)
    daily_food_menu_list = await food_menu_fetch_interactor.execute()

    food_menu_for_specific_day_pick_interactor = (
        FoodMenuForSpecificDayPickInteractor(
            daily_food_menu_list=daily_food_menu_list,
            days_to_skip=days_to_skip,
        )
    )
    daily_food_menu = food_menu_for_specific_day_pick_interactor.execute()

    if daily_food_menu is None:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyFoodMenuView(daily_food_menu)
    await answer_media_group_view(message, view)

    with sqlite3.connect("./usage_statistics.db") as connection:
        dao = UsageStatisticsDao(connection=connection)
        interactor = TrackUsageInteractor(usage_statistics_dao=dao)
        interactor.execute(user_id=user_id, chat_id=chat_id)
