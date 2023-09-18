import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from bot.constants.messages import ASSISTANCE_MESSAGE
from bot.keyboards.menu import support_keyboard

# Инициализация логгера
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /start."""
    keyboards = [[support_keyboard()]]
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Please choose:", reply_markup=reply_markup
    )


async def support_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /support."""
    await update.callback_query.edit_message_text(ASSISTANCE_MESSAGE)


HANDLERS = CommandHandler("start", start_bot)
support_bot_handler = CallbackQueryHandler(support_bot)
