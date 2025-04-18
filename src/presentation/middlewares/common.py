from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update
from aiogram.enums import ChatType


type Handler = Callable[[Update, dict[str, Any]], Awaitable[Any]]
type ContextData = dict[str, Any]


def get_chat_type(event: Update) -> ChatType | str | None:
    """
    Get the chat type from the event.
    """
    if event.message is not None and event.message.chat is not None:
        return event.message.chat.type
    if (
        event.callback_query is not None
        and event.callback_query.message is not None
    ):
        return event.callback_query.message.chat.type
    return None


def get_user_id(event: Update) -> int | None:
    """
    Get the user ID from the event.
    """
    if event.message is not None and event.message.from_user is not None:
        return event.message.from_user.id
    if (
        event.callback_query is not None
        and event.callback_query.from_user is not None
    ):
        return event.callback_query.from_user.id
    return None


def get_chat_id(event: Update) -> int | None:
    """
    Get the chat ID from the event.
    """
    if event.message is not None and event.message.chat is not None:
        return event.message.chat.id
    if (
        event.callback_query is not None
        and event.callback_query.message is not None
    ):
        return event.callback_query.message.chat.id
    return None
