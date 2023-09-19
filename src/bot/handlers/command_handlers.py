from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import ASSISTANCE_MESSAGE, START_MESSAGE
from bot.keyboards.command_keyboards import (
    start_keyboard_markup,
    support_keyboard_markup,
)


async def start(update: Update, context: CallbackContext) -> None:
    """Функция-обработчик команды start."""
    await update.message.reply_text(
        text=START_MESSAGE, reply_markup=start_keyboard_markup
    )


async def support_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /support."""
    await update.message.reply_text(
        text=ASSISTANCE_MESSAGE, reply_markup=support_keyboard_markup
    )


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
