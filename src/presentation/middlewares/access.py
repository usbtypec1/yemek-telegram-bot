from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

from presentation.middlewares.common import (
    Handler,
    get_chat_id,
    get_user_id,
)


class AccessMiddleware(BaseMiddleware):
    def __init__(self, chat_id: int, access_denied_text: str) -> None:
        self.__chat_id = chat_id
        self.__access_denied_text = access_denied_text

    async def __call__(
        self,
        handler: Handler,
        event: Update,
        data: dict[str, Any],
    ):
        user_id = get_user_id(event)
        chat_id = get_chat_id(event)

        if user_id is None or chat_id is None:
            return await handler(event, data)

        bot: Bot = data["bot"]

        chat_member = await bot.get_chat_member(
            chat_id=self.__chat_id,
            user_id=user_id,
        )

        if (
            chat_member.status == ChatMemberStatus.LEFT
            or chat_member.status == ChatMemberStatus.KICKED
        ):
            await bot.send_message(
                chat_id=chat_id,
                text=self.__access_denied_text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="👌 Я подписался",
                                callback_data="start",
                            )
                        ]
                    ]
                ),
            )
            return

        return await handler(event, data)
