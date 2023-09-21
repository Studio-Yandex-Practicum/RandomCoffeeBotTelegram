from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from bot.constants.messages import (
    ASSISTANCE_MESSAGE,
    HELP_MESSAGE,
    START_MESSAGE,
)
from bot.keyboards.command_keyboards import (
    help_keyboard_markup,
    start_keyboard_markup,
    support_keyboard_markup,
)
from core.config.logging import log_handler


@log_handler
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


@log_handler
async def help(update: Update, context: CallbackContext) -> None:
    """Функция-обработчик для команды /help."""
    await update.message.reply_html(
        text=(HELP_MESSAGE), reply_markup=help_keyboard_markup
    )


async def keyboard_collback_handler(
    update: Update, context: CallbackContext
) -> None:
    """Функция-обработчик для команд."""
    query = update.callback_query
    if query.data == "support":
        await query.edit_message_text(
            text=ASSISTANCE_MESSAGE, reply_markup=support_keyboard_markup
        )


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
collback_handler = CallbackQueryHandler(keyboard_collback_handler)
