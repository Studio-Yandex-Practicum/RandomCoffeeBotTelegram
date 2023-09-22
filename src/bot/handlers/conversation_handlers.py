from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.constants.messages import (
    CHOOSE_ROLE_MESSAGE,
    GUESS_NAME_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.keyboards.conversation_keyboards import (
    guess_name_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import Recruiter, Student


async def go(update: Update, context: CallbackContext):
    """Обработчик кнопки "GO"."""
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    if not (
        await Recruiter.objects.filter(telegram_id=user.id).aexists()
        or await Student.objects.filter(telegram_id=user.id).aexists()
    ):
        await query.edit_message_text(CHOOSE_ROLE_MESSAGE)
        await query.edit_message_reply_markup(role_choice_keyboard_markup)
        return States.ROLE_CHOICE
    else:
        await query.message.reply_text(PAIR_SEARCH_MESSAGE)
        return ConversationHandler.END  # Тут будет States.PAIR_SEARCH


async def next_time(update: Update, context: CallbackContext):
    """Обработчик кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(NEXT_TIME_MESSAGE)
    await query.edit_message_reply_markup(reply_markup=restart_keyboard_markup)
    return States.NEXT_TIME


async def restart_callback(update: Update, context: CallbackContext):
    """Обработчик для кнопки start."""
    query = update.callback_query
    await query.answer()
    return await start(update, context)


async def role_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора роли."""
    query = update.callback_query
    context.user_data["role"] = query.data
    guessed_name = query.from_user.first_name
    await query.answer()
    await query.edit_message_text(GUESS_NAME_MESSAGE.format(guessed_name))
    await query.edit_message_reply_markup(guess_name_keyboard_markup)
    return ConversationHandler.END
