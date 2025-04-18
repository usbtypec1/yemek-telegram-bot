from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command, or_f

from presentation.ui.views.base import answer_view
from presentation.ui.views.food_menu import (
    UserPrivateChatMenuView,
)

router = Router(name=__name__)


@router.callback_query(
    F.data == "start",
    F.message.chat.type == ChatType.PRIVATE,
)
async def on_start_callback_in_private_chat(
    callback_query: CallbackQuery,
) -> None:
    message: Message = callback_query.message  # type: ignore
    view = UserPrivateChatMenuView()
    await answer_view(message, view)
    await callback_query.answer()


@router.message(
    or_f(
        CommandStart(),
    ),
    F.chat.type == ChatType.PRIVATE,
)
async def on_help_command_in_private_chat(
    message: Message,
) -> None:
    view = UserPrivateChatMenuView()
    await answer_view(message, view)
