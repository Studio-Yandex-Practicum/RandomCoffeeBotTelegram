import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

# Инициализация логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция-обработчик для команды /start
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_html(
        fr'Привет, {user.mention_html()}!',
        parse_mode='HTML',
    )

HANDLERS = CommandHandler("start", start)
