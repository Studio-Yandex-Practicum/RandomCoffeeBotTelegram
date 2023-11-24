from typing import Literal

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import (
    ASSISTANCE_MESSAGE,
    CONFIRMATION_DELETE_ACCOUNT_MESSAGE,
    HELP_MESSAGE,
    NOT_REGISTRED_MESSAGE,
    START_MESSAGE,
)
from bot.constants.states import States
from bot.keyboards.command_keyboards import (
    create_support_keyboard,
    delete_keyboard_markup,
    help_keyboard_markup,
    start_keyboard_markup,
)
from bot.keyboards.conversation_keyboards import restart_keyboard_markup
from bot.utils.db_utils.user import update_last_login_date, user_is_exist
from core.config.logging import debug_logger


@debug_logger
async def start(
    update: Update, context: CallbackContext
) -> Literal[States.START]:
    """Функция-обработчик команды start."""
    # user = update.message.from_user
    # if user and await user_is_exist(user.id):
    #     await update_last_login_date(user.id)

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
    user = update.message.from_user
    if user and await user_is_exist(user.id):
        await update_last_login_date(user.id)

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
    user = update.message.from_user
    if user and await user_is_exist(user.id):
        await update_last_login_date(user.id)

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


@debug_logger
async def start_delete_account(update: Update, context: CallbackContext):
    """Обработчик удаления аккаунта."""
    user = update.message.from_user
    profession = context.user_data["profession"]
    if user and await user_is_exist(user.id):
        await update.message.reply_text(
            text=CONFIRMATION_DELETE_ACCOUNT_MESSAGE.format(profession),
            reply_markup=delete_keyboard_markup,
        )
        return States.DELETE_ACCOUNT
    else:
        await update.message.reply_text(
            text=NOT_REGISTRED_MESSAGE, reply_markup=restart_keyboard_markup
        )
        return States.NOT_REGISTERED


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
delete_handler = CommandHandler("delete_account", start_delete_account)
