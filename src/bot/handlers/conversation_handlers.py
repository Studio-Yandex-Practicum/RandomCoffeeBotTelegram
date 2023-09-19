from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.constants.buttons import CHOOSE_ROLE_BUTTON
from bot.constants.messages import (
    CHOOSE_ROLE_MESSAGE,
    GUESS_NAME_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
)
from bot.constants.states import States
from bot.keyboards.conversation_keyboards import guess_name_keyboard_markup
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
        await query.message.reply_text(
            text=CHOOSE_ROLE_MESSAGE,
            reply_markup=ReplyKeyboardMarkup(
                [CHOOSE_ROLE_BUTTON],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        return States.ROLE_CHOICE
    else:
        await query.message.reply_text(PAIR_SEARCH_MESSAGE)
        return ConversationHandler.END  # Тут будет States.PAIR_SEARCH


async def next_time(update: Update, context: CallbackContext):
    """Обработчик кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(NEXT_TIME_MESSAGE, reply_markup=None)
    return ConversationHandler.END


async def role_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора роли."""
    context.user_data["choice"] = update.message.text
    guessed_name = update.message.from_user.name.replace("@", "", 1)
    await update.message.reply_text(
        GUESS_NAME_MESSAGE.format(guessed_name),
        reply_markup=guess_name_keyboard_markup,
    )
    return ConversationHandler.END
