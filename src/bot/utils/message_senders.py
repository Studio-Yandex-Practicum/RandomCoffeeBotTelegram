from telegram.ext import CallbackContext

from bot.constants.messages import (
    IS_PAIR_SUCCESSFUL_MESSAGE,
    USER_DELETE_MESSAGE,
)
from bot.keyboards.conversation_keyboards import (
    is_pair_successful_keyboard_markup,
)
from core.config.logging import debug_logger


@debug_logger
async def send_is_pair_successful_message(context: CallbackContext):
    """Отправляет сообщение состоялся ли звонок."""
    await context.bot.send_message(
        chat_id=context.job.user_id,
        text=IS_PAIR_SUCCESSFUL_MESSAGE,
        reply_markup=is_pair_successful_keyboard_markup,
    )


@debug_logger
async def send_deleting_from_db_message(context: CallbackContext):
    """Отправляет сообщение об удалении из базы данных."""
    await context.bot.send_message(
        chat_id=context.job.user_id,
        text=USER_DELETE_MESSAGE.format(context.job.data),
    )
