from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import START_MESSAGE
from bot.constants.states import States
from bot.keyboards.command_keyboards import start_keyboard_markup


async def start(update: Update, context: CallbackContext):
    """Функция-обработчик команды start."""
    await update.message.reply_text(
        START_MESSAGE, reply_markup=start_keyboard_markup
    )

    return States.START


start_handler = CommandHandler("start", start)
