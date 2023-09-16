import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import HELP_MESSAGE
from bot.keyboards.help_keyboard import help_keyboard

# Инициализация логгера
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /start."""
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}!")


async def help_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /help."""
    await update.message.reply_html(
        text=(HELP_MESSAGE), reply_markup=help_keyboard
    )


HANDLERS = CommandHandler("start", start_bot)
HELP_COMMAND = CommandHandler("help", help_bot)
