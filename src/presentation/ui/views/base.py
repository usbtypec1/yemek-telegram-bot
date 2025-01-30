from typing import TypeAlias, assert_never

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.media_group import MediaGroupBuilder, MediaType

__all__ = (
    "ReplyMarkup",
    "TextView",
    "answer_text_view",
    "edit_message_by_view",
    "answer_or_edit_message_by_view",
    "send_text_view",
    "answer_media_group_view",
    "MediaGroupView",
    "PhotoView",
    "answer_photo_view",
    "send_photo_view",
    "answer_view",
    "View",
    "send_view",
)

ReplyMarkup: TypeAlias = (
    InlineKeyboardMarkup
    | ReplyKeyboardMarkup
    | ForceReply
    | ReplyKeyboardRemove
)


class PhotoView:
    photo: str | None = None
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_photo(self) -> str | None:
        return self.photo

    def get_caption(self) -> str | None:
        return self.caption

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class TextView:
    text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class MediaGroupView:
    medias: list[MediaType] | None = None
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_caption(self) -> str | None:
        return self.caption

    def get_medias(self) -> list[MediaType] | None:
        return self.medias

    def as_media_group(self) -> list[MediaType]:
        media_group_builder = MediaGroupBuilder(
            media=self.get_medias(),
            caption=self.get_caption(),
        )
        return media_group_builder.build()

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


View: TypeAlias = TextView | PhotoView | MediaGroupView


async def answer_text_view(message: Message, view: TextView) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_photo_view(message: Message, view: PhotoView) -> Message:
    return await message.answer_photo(
        photo=view.get_photo(),
        caption=view.get_caption(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_media_group_view(
    message: Message,
    view: MediaGroupView,
) -> list[Message]:
    return await message.answer_media_group(
        media=view.as_media_group(),
    )


async def answer_view(message: Message, view: View) -> Message | list[Message]:
    match view:
        case TextView():
            return await answer_text_view(message, view)
        case PhotoView():
            return await answer_photo_view(message, view)
        case MediaGroupView():
            return await answer_media_group_view(message, view)
        case _:
            assert_never(view)


async def edit_message_by_view(message: Message, view: TextView) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_or_edit_message_by_view(
    message_or_callback_query: Message | CallbackQuery,
    view: TextView,
) -> Message:
    if isinstance(message_or_callback_query, Message):
        return await answer_text_view(message_or_callback_query, view)
    return await edit_message_by_view(message_or_callback_query.message, view)


async def send_text_view(
    bot: Bot,
    view: TextView,
    *chat_ids: int,
) -> list[Message | None]:
    text = view.get_text()
    reply_markup = view.get_reply_markup()
    result = []
    for chat_id in chat_ids:
        try:
            result.append(
                await bot.send_message(chat_id, text, reply_markup=reply_markup)
            )
        except TelegramAPIError:
            result.append(None)
    return result


async def send_photo_view(
    bot: Bot,
    view: PhotoView,
    *chat_ids: int,
) -> list[Message | None]:
    caption = view.get_caption()
    photo = view.get_photo()
    reply_markup = view.get_reply_markup()
    result = []
    for chat_id in chat_ids:
        try:
            result.append(
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            )
        except TelegramAPIError:
            result.append(None)
    return result


async def send_view(
    bot: Bot,
    view: View,
    *chat_ids: int,
) -> list[Message | None]:
    match view:
        case TextView():
            return await send_text_view(bot, view, *chat_ids)
        case PhotoView():
            return await send_photo_view(bot, view, *chat_ids)
        case _:
            assert_never(view)
