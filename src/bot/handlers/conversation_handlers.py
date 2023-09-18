from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.constants.messages import NEXT_TIME_MESSAGE


async def go(update: Update, context: CallbackContext):
    """123."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Тут будет логика для GO")
    return ConversationHandler.END  # пока что так, чтобы бот не зависал


async def next_time(update: Update, context: CallbackContext):
    """1234."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(NEXT_TIME_MESSAGE, reply_markup=None)
    return ConversationHandler.END
