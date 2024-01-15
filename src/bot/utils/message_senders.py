from datetime import timedelta

from django.utils import timezone
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.keyboards.conversation_keyboards import (
    guess_name_keyboard_markup,
    is_pair_successful_keyboard_markup,
)
from bot.utils.correction_name_or_surname import correction_name_or_surname
from bot.utils.db_utils.message import get_message_bot
from bot.utils.db_utils.pair import delete_pair, get_active_pair
from core.config.logging import debug_logger

LAST_TIME = 2


@debug_logger
async def send_is_pair_successful_message(context: CallbackContext) -> None:
    """Отправляет сообщение состоялся ли звонок."""
    if context.job:
        context.user_data["job"] = context.job
        question_call_day_in_seconds = context.job.data.get("first")
        final_response_time = (
            context.job.data.get("start_time")
            + timedelta(days=LAST_TIME)
            + timedelta(seconds=question_call_day_in_seconds)
        )
        if timezone.now() < final_response_time:
            text = await get_message_bot("is_pair_successful_message")
            await context.bot.send_message(
                chat_id=context.job.user_id,
                text=text,
                reply_markup=is_pair_successful_keyboard_markup,
                parse_mode=ParseMode.HTML,
            )
        elif timezone.now() >= final_response_time:
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
        text = await get_message_bot("user_delete_message")
        await context.bot.send_message(
            chat_id=context.job.user_id,
            text=text.format(context.job.data),
            parse_mode=ParseMode.HTML,
        )


@debug_logger
async def send_name_message(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с именем."""
    query = update.callback_query
    if context.user_data:
        guessed_name = correction_name_or_surname(
            str(
                context.user_data.get(
                    "name", query.from_user.first_name if query else "unknown"
                )
            )
        )
    if query:
        text = await get_message_bot("guess_name_message")
        context.user_data["name"] = guessed_name
        await query.answer()
        await query.edit_message_text(
            text.format(guessed_name),
            parse_mode=ParseMode.HTML,
        )
        await query.edit_message_reply_markup(guess_name_keyboard_markup)
    elif update.message:
        text = await get_message_bot("guess_name_message")
        await update.message.reply_text(
            text.format(guessed_name),
            reply_markup=guess_name_keyboard_markup,
            parse_mode=ParseMode.HTML,
        )
