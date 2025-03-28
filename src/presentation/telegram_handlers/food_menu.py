import sqlite3
from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, StateFilter, Command, and_f, or_f
from aiogram.types import CallbackQuery, Message

from infrastructure.usage_statistics import UsageStatisticsDao
from presentation.ui.views.base import answer_media_group_view, answer_view
from presentation.ui.views.food_menu import (
    DailyFoodMenuView,
    FoodMenuHelpView,
    UserPrivateChatMenuView,
)
from presentation.callback_data.food_menu import FoodMenuCallbackData
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
    Command("statistics"),
    StateFilter("*"),
)
async def on_show_statistics(message: Message) -> None:
    text = "Пользователь - количество"
    with sqlite3.connect("./usage_statistics.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id, COUNT(*) FROM usages GROUP BY user_id ORDER BY COUNT(*) DESC;"
        )
        for user_id, count in cursor.fetchall():
            text += f"\n{user_id} - {count}"
    await message.answer(text)


@router.callback_query(
    FoodMenuCallbackData.filter(),
    StateFilter("*"),
)
async def on_show_food_menu_for_specific_day_by_button(
    callback_query: CallbackQuery,
    callback_data: FoodMenuCallbackData,
    food_menu_cache: FoodMenuCache,
    food_menu_cleaner_queue: FoodMenuCleanerQueue,
) -> None:
    message: Message = callback_query.message  # type: ignore
    user_id = callback_query.message.from_user.id  # type: ignore
    chat_id = callback_query.message.chat.id  # type: ignore

    food_menu_fetch_interactor = FoodMenuFetchInteractor(cache=food_menu_cache)
    daily_food_menu_list = await food_menu_fetch_interactor.execute()

    food_menu_for_specific_day_pick_interactor = (
        FoodMenuForSpecificDayPickInteractor(
            daily_food_menu_list=daily_food_menu_list,
            days_to_skip=callback_data.days_to_skip,
        )
    )
    daily_food_menu = food_menu_for_specific_day_pick_interactor.execute()

    if daily_food_menu is None:
        await callback_query.answer(
            "Нет данных за указанный день 😔", show_alert=True
        )
        return

    view = DailyFoodMenuView(daily_food_menu)
    messages = await answer_media_group_view(message, view)
    await message.delete()

    if callback_query.message.chat.type in (
        ChatType.GROUP,
        ChatType.SUPERGROUP,
    ):
        await food_menu_cleaner_queue.add(
            chat_id=chat_id,
            message_ids=[message.message_id for message in messages]
            + [callback_query.message.message_id],
        )
    with sqlite3.connect("./usage_statistics.db") as connection:
        dao = UsageStatisticsDao(connection=connection)
        interactor = TrackUsageInteractor(usage_statistics_dao=dao)
        interactor.execute(user_id=user_id, chat_id=chat_id)


@router.message(
    or_f(
        F.text.lower().startswith("йемек "),
        F.text.lower().startswith("yemek "),
        F.text.lower().startswith("емек "),
        F.text.lower().startswith("/yemek "),
        F.text.in_(("🕕 Сегодня", "🕒 Завтра", "🕞 Послезавтра")),
    ),
    StateFilter("*"),
)
async def on_show_food_menu_for_specific_day_by_command(
    message: Message,
    food_menu_cache: FoodMenuCache,
    food_menu_cleaner_queue: FoodMenuCleanerQueue,
):
    user_id = message.from_user.id  # type: ignore
    chat_id = message.chat.id  # type: ignore
    message_text: str = message.text  # type: ignore

    word_to_days_count = {
        "сегодня": 0,
        "завтра": 1,
        "послезавтра": 2,
        "today": 0,
        "tomorrow": 1,
        "🕕 Сегодня": 0,
        "🕒 Завтра": 1,
        "🕞 Послезавтра": 2,
    }

    if message_text in word_to_days_count:
        days_to_skip = word_to_days_count[message_text]
    else:
        for command in ("йемек на", "йемек", "емек на", "емек", "yemek"):
            if message_text.strip("/").lower().startswith(command):
                days_to_skip = message_text.strip("/")[len(command) :].strip()
                break
        else:
            return

        if days_to_skip.isdigit():
            days_to_skip = int(days_to_skip)
        elif days_to_skip in word_to_days_count:
            days_to_skip = word_to_days_count[days_to_skip]
        else:
            await message.reply("Не могу распознать день 😔")
            return

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
    messages = await answer_media_group_view(message, view)

    if message.chat.type in (
        ChatType.GROUP,
        ChatType.SUPERGROUP,
    ):
        await food_menu_cleaner_queue.add(
            chat_id=chat_id,
            message_ids=[message.message_id for message in messages]
            + [message.message_id],
        )

    with sqlite3.connect("./usage_statistics.db") as connection:
        dao = UsageStatisticsDao(connection=connection)
        interactor = TrackUsageInteractor(usage_statistics_dao=dao)
        interactor.execute(user_id=user_id, chat_id=chat_id)


@router.callback_query(
    F.data == "start",
    StateFilter("*"),
)
async def on_start(callback_query: CallbackQuery) -> None:
    if callback_query.message.chat.type == ChatType.PRIVATE:
        view = UserPrivateChatMenuView()
    else:
        view = FoodMenuHelpView()
    await answer_view(callback_query.message, view)
    await callback_query.message.delete()
    await callback_query.answer()


@router.message(
    or_f(
        Command("yemek"),
        F.text.lower().in_(("yemek", "йемек", "емек")),
        and_f(
            CommandStart(),
            F.chat.type == ChatType.PRIVATE,
        ),
    ),
    StateFilter("*"),
)
async def on_show_food_menu_help(message: Message) -> None:
    if message.chat.type == ChatType.PRIVATE:
        view = UserPrivateChatMenuView()
    else:
        view = FoodMenuHelpView()
    await answer_view(message, view)
