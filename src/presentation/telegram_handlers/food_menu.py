from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from infrastructure.adapters.food_menu_items import FoodMenuItemGateway
from presentation.ui.views.base import answer_media_group_view, answer_view
from presentation.ui.views.food_menu import (
    DailyFoodMenuView,
    UserPrivateChatMenuView,
)
from application.interactors.food_menu_for_specific_day import (
    FoodMenuForSpecificDayPickInteractor,
)
from application.interactors.track_usage import TrackUsageInteractor


router = Router(name=__name__)


@router.message(
    F.text.in_(("🕕 Сегодня", "🕒 Завтра", "🕞 Послезавтра")),
)
async def on_show_food_menu_for_specific_day(
    message: Message,
    food_menu_item_gateway: FromDishka[FoodMenuItemGateway],
):
    word_to_days_count = {
        "🕕 Сегодня": 0,
        "🕒 Завтра": 1,
        "🕞 Послезавтра": 2,
    }
    days_to_skip: int = word_to_days_count[message.text]  # type: ignore

    daily_food_menu = await FoodMenuForSpecificDayPickInteractor(
        food_menu_item_gateway=food_menu_item_gateway,
        days_to_skip=days_to_skip,
    ).execute()

    if not daily_food_menu.items:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyFoodMenuView(daily_food_menu)
    await answer_media_group_view(message, view)


@router.message(
    Command("yemek"),
)
async def on_show_food_menu_for_specific_day_by_command(
    message: Message,
    command: CommandObject,
    food_menu_item_gateway: FromDishka[FoodMenuItemGateway],
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

    if command.args in word_to_days_count:
        days_to_skip = word_to_days_count[command.args]
    elif command.args.isdigit():
        days_to_skip = int(command.args)
    else:
        await message.reply("Не могу распознать день 😔")
        return
    
    daily_food_menu = await FoodMenuForSpecificDayPickInteractor(
        food_menu_item_gateway=food_menu_item_gateway,
        days_to_skip=days_to_skip,
    ).execute()

    if not daily_food_menu.items:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyFoodMenuView(daily_food_menu)
    await answer_media_group_view(message, view)
