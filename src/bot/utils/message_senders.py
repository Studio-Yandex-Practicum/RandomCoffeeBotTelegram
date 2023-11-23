from telegram import Update
from telegram.ext import CallbackContext

from bot.constants.messages import (
    GUESS_NAME_MESSAGE,
    IS_PAIR_SUCCESSFUL_MESSAGE,
    USER_DELETE_MESSAGE,
)
from bot.keyboards.conversation_keyboards import (
    guess_name_keyboard_markup,
    is_pair_successful_keyboard_markup,
)
from core.config.logging import debug_logger


@debug_logger
async def send_is_pair_successful_message(context: CallbackContext) -> None:
    """Отправляет сообщение состоялся ли звонок."""
    if context.job:
        await context.bot.send_message(
            chat_id=context.job.user_id,
            text=IS_PAIR_SUCCESSFUL_MESSAGE,
            reply_markup=is_pair_successful_keyboard_markup,
        )


@debug_logger
async def send_deleting_from_db_message(context: CallbackContext) -> None:
    """Отправляет сообщение об удалении из базы данных."""
    if context.job:
        await context.bot.send_message(
            chat_id=context.job.user_id,
            text=USER_DELETE_MESSAGE.format(context.job.data),
        )


@debug_logger
async def send_name_message(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с именем."""
    query = update.callback_query
    if context.user_data:
        guessed_name = context.user_data.get(
            "name", query.from_user.first_name if query else "unknown"
        )
    if query:
        context.user_data["name"] = guessed_name
        await query.answer()
        await query.edit_message_text(GUESS_NAME_MESSAGE.format(guessed_name))
        await query.edit_message_reply_markup(guess_name_keyboard_markup)
    elif update.message:
        await update.message.reply_text(
            GUESS_NAME_MESSAGE.format(guessed_name),
            reply_markup=guess_name_keyboard_markup,
        )
