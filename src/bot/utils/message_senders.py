from datetime import timedelta

from django.utils import timezone
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
from bot.utils.db_utils.pair import delete_pair, get_active_pair
from core.config.logging import debug_logger

TIME_SECOND_PING = 7
LAST_TIME = 10


@debug_logger
async def send_is_pair_successful_message(context: CallbackContext) -> None:
    """Отправляет сообщение состоялся ли звонок."""
    if context.job:
        context.user_data["job"] = context.job
        await context.bot.send_message(
            chat_id=context.job.user_id,
            text=IS_PAIR_SUCCESSFUL_MESSAGE,
            reply_markup=is_pair_successful_keyboard_markup,
        )
        context.job.job.reschedule(
            trigger="interval", seconds=TIME_SECOND_PING
        )
        if timezone.now() > context.job.data.get("start_time") + timedelta(
            seconds=LAST_TIME
        ):
            pair = await get_active_pair(
                context.user_data.get("role"), context.job.user_id
            )
            if pair:
                await delete_pair(pair.itspecialist, pair.recruiter, False)
            context.job.job.remove()


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
