from telegram import Update
from telegram.ext import CallbackContext

from bot.constants.messages import NEXT_TIME_MESSAGE
from bot.constants.states import States


async def go(update: Update, context: CallbackContext):
    """123."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Тут будет логика для GO")


async def next_time(update: Update, context: CallbackContext):
    """1234."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(NEXT_TIME_MESSAGE)
    return States.NEXT_TIME
