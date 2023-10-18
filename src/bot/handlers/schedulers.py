from telegram.ext import CallbackContext

from bot.constants.messages import IS_PAIR_SUCCESSFUL_MESSAGE
from bot.keyboards.conversation_keyboards import (
    is_pair_successful_keyboard_markup,
)
from core.config.logging import log_info


@log_info
async def send_is_pair_successful_message(context: CallbackContext):
    """Отправляет сообщение состоялся ли звонок."""
    await context.bot.send_message(
        chat_id=context.job.user_id,
        text=IS_PAIR_SUCCESSFUL_MESSAGE,
        reply_markup=is_pair_successful_keyboard_markup,
    )
