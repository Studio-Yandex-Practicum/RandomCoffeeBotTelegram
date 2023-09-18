from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from bot.constants.messages import ASSISTANCE_MESSAGE, START_MESSAGE
from bot.keyboards.command_keyboards import (
    start_keyboard_markup,
    support_keyboard,
)


async def menu_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /menu."""
    keyboards = [[support_keyboard()]]
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Please choose:", reply_markup=reply_markup
    )


async def start(update: Update, context: CallbackContext) -> None:
    """Функция-обработчик команды start."""
    await update.message.reply_text(
        text=START_MESSAGE, reply_markup=start_keyboard_markup
    )


async def support_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /support."""
    await update.callback_query.edit_message_text(ASSISTANCE_MESSAGE)


menu_handler = CommandHandler("menu", menu_bot)
start_handler = CommandHandler("start", start)
support_bot_handler = CallbackQueryHandler(support_bot)
