from aiogram.enums import ChatType
from aiogram.types import TelegramObject, Update, User

from presentation.middlewares.common import (
    ContextData,
    Handler,
    get_chat_type,
)


async def group_chat_warning_middleware(
    handler: Handler,
    event: TelegramObject,
    data: ContextData,
) -> None:
    """
    Middleware to warn users about group chat access.
    """
    update: Update = event  # type: ignore
    chat_type = get_chat_type(update)

    if chat_type == ChatType.PRIVATE:
        return await handler(update, data)

    if update.message is not None:
        if not (
            update.message.text is not None
            and update.message.text.startswith("/")
        ):
            return

    bot_user: User = data["bot_user"]

    text = f"❗️ Чтобы использовать бота, перейдите в ЛС @{bot_user.username}"

    if update.message is not None:
        await update.message.answer(text)
    elif update.callback_query is not None:
        await update.callback_query.answer(
            text,
            show_alert=True,
        )
