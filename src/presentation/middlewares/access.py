from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus


class AccessMiddleware(BaseMiddleware):
    def __init__(self, chat_id: int, access_denied_text: str) -> None:
        self.__chat_id = chat_id
        self.__access_denied_text = access_denied_text

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ):
        user_id: int | None = None
        if event.message is not None:
            if event.message.from_user is not None:
                user_id = event.message.from_user.id
        if event.callback_query is not None:
            if event.callback_query.from_user is not None:
                user_id = event.callback_query.from_user.id

        if user_id is None:
            return await handler(event, data)

        bot: Bot = data["bot"]

        chat_member = await bot.get_chat_member(
            chat_id=self.__chat_id, user_id=user_id
        )

        if (
            chat_member.status == ChatMemberStatus.LEFT
            or chat_member.status == ChatMemberStatus.KICKED
        ):
            await bot.send_message(
                chat_id=user_id,
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
