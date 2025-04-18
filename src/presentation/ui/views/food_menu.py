from aiogram.types import (
    InputMediaPhoto,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.media_group import MediaType

from presentation.ui.views.base import MediaGroupView, TextView
from domain.entities import DailyFoodMenu
from domain.services.date import get_weekday_name


class DailyFoodMenuView(MediaGroupView):
    def __init__(self, daily_food_menu: DailyFoodMenu) -> None:
        self.__daily_food_menu = daily_food_menu

    def get_medias(self) -> list[MediaType]:
        return [
            InputMediaPhoto(media=item.photo_url)
            for item in self.__daily_food_menu.items
        ]

    def get_caption(self) -> str:
        weekday_name = get_weekday_name(self.__daily_food_menu.at)
        lines: list[str] = [
            f"<b>🍽️ Меню на {self.__daily_food_menu.at:%d.%m.%Y} ({weekday_name}) 🍽️</b>"
        ]
        for item in self.__daily_food_menu.items:
            lines.append(f"\n🧂 <u>{item.name}</u>")
            lines.append(f"🌱 Калории: {item.calories_count}")

        total_calories_count = sum(
            item.calories_count for item in self.__daily_food_menu.items
        )

        lines.append(f"\n🔥 <b>Сумма калорий: {total_calories_count}</b>")
        return "\n".join(lines)


class UserPrivateChatMenuView(TextView):
    text = (
        "<b>🤤 Просмотр меню в йемекхане:</b>"
        "\n\n🍏 На сегодня:"
        "\n<code>/yemek today</code>"
        "\n\n🍏 На завтра:"
        "\n<code>/yemek tomorrow</code>"
        "\n\n<b>🧐 Так же можно просматривать на N дней вперёд:</b>"
        "\n<code>/yemek {N}</code>"
        "\n\nНапример👇"
        "\n🍎 На послезавтра - /yemek 2"
        "\n🍎 10 дней вперёд - /yemek 10"
        "\n\n<b>👇 Так же можете посмотреть меню на веб странице:</b>"
        "\nhttps://t.me/duck_duck_robot/yemek"
    )
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text="🕕 Сегодня",
                ),
                KeyboardButton(
                    text="🕒 Завтра",
                ),
            ],
            [
                KeyboardButton(
                    text="🕞 Послезавтра",
                ),
            ],
        ],
    )
