from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus, ChatType


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
        chat_id: int | None = None
        message_text: str | None = None
        chat_type: str | None = None
        if event.message is not None:
            if event.message.from_user is not None:
                user_id = event.message.from_user.id
                chat_id = event.message.chat.id
                message_text = event.message.text
                chat_type = event.message.chat.type
        if event.callback_query is not None:
            if (
                event.callback_query.from_user is not None
                and event.callback_query.message is not None
            ):
                user_id = event.callback_query.from_user.id
                chat_id = event.callback_query.message.chat.id
                chat_type = event.callback_query.message.chat.type

        if user_id is None or chat_id is None:
            return await handler(event, data)

        bot: Bot = data["bot"]

        if (
            message_text is not None
            and not message_text.startswith("/")
            and chat_type
            in (
                ChatType.GROUP,
                ChatType.SUPERGROUP,
            )
        ):
            return await handler(event, data)

        chat_member = await bot.get_chat_member(
            chat_id=self.__chat_id, user_id=user_id
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
