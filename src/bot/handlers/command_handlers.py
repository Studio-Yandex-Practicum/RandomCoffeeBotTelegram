from typing import Literal

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import (
    ASSISTANCE_MESSAGE,
    HELP_MESSAGE,
    START_MESSAGE,
)
from bot.constants.states import States
from bot.keyboards.command_keyboards import (
    create_support_keyboard,
    help_keyboard_markup,
    start_keyboard_markup,
)
from core.config.logging import debug_logger


@debug_logger
async def start(
    update: Update, context: CallbackContext
) -> Literal[States.START]:
    """Функция-обработчик команды start."""
    if update.message:
        await update.message.reply_text(
            text=START_MESSAGE, reply_markup=start_keyboard_markup
        )
    return States.START


@debug_logger
async def support_bot(
    update: Update, context: CallbackContext
) -> Literal[States.SUPPORT]:
    """Функция-обработчик для команды /support."""
    if update.message:
        await update.message.reply_text(
            text=ASSISTANCE_MESSAGE,
            reply_markup=await create_support_keyboard(),
        )
    return States.SUPPORT


@debug_logger
async def help(
    update: Update, context: CallbackContext
) -> Literal[States.HELP]:
    """Функция-обработчик для команды /help."""
    if update.message:
        await update.message.reply_html(
            text=(HELP_MESSAGE), reply_markup=help_keyboard_markup
        )
    return States.HELP


@debug_logger
async def redirection_to_support(
    update: Update, context: CallbackContext
) -> None:
    """Перенаправление на команду /support."""
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=ASSISTANCE_MESSAGE,
            reply_markup=await create_support_keyboard(),
        )


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
