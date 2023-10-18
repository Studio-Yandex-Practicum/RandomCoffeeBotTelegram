from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import (
    ASSISTANCE_MESSAGE,
    HELP_MESSAGE,
    START_MESSAGE,
)
from bot.constants.states import States
from bot.keyboards.command_keyboards import (
    help_keyboard_markup,
    start_keyboard_markup,
    support_keyboard_markup,
)
from core.config.logging import log_info


@log_info
async def start(update: Update, context: CallbackContext):
    """Функция-обработчик команды start."""
    if update.message:
        await update.message.reply_text(
            text=START_MESSAGE, reply_markup=start_keyboard_markup
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            START_MESSAGE, reply_markup=start_keyboard_markup
        )

    return States.START


@log_info
async def support_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /support."""
    await update.message.reply_text(
        text=ASSISTANCE_MESSAGE, reply_markup=support_keyboard_markup
    )


@log_info
async def help(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /help."""
    await update.message.reply_html(
        text=(HELP_MESSAGE), reply_markup=help_keyboard_markup
    )
    return States.HELP


@log_info
async def redirection_to_support(
    update: Update, context: CallbackContext
) -> None:
    """Перенаправление на команду /support."""
    query = update.callback_query
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=support_keyboard_markup
    )


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
