import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

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


HANDLERS = CommandHandler("start", start_bot)
