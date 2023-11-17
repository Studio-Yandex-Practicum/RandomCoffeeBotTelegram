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
from bot.models import Recruiter, Student
from core.config.logging import debug_logger


@debug_logger
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


@debug_logger
async def support_bot(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /support."""
    await update.message.reply_text(
        text=ASSISTANCE_MESSAGE, reply_markup=await create_support_keyboard()
    )


@debug_logger
async def help(update: Update, context: CallbackContext):
    """Функция-обработчик для команды /help."""
    await update.message.reply_html(
        text=(HELP_MESSAGE), reply_markup=help_keyboard_markup
    )
    return States.HELP


@debug_logger
async def redirection_to_support(
    update: Update, context: CallbackContext
) -> None:
    """Перенаправление на команду /support."""
    query = update.callback_query
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=await create_support_keyboard()
    )


@debug_logger
async def delete_account(update: Update, context: CallbackContext):
    """Обработчик удаления аккаунта."""
    user = update.message.from_user
    profession = context.user_data["profession"]
    if user and await user_is_exist(user.id):
        await update.message.reply_text(
            text=CONFIRMATION_DELETE_ACCOUNT_MESSAGE.format(profession),
            reply_markup=delete_keyboard_markup,
        )
    else:
        await update.message.reply_text(
            text=NOT_REGISTRED_MESSAGE, reply_markup=restart_keyboard_markup
        )
        return States.START


async def user_is_exist(user_id: int) -> bool:
    """Проверяет наличие юзера в базе данных."""
    if (
        await Recruiter.objects.filter(telegram_id=user_id).aexists()
        or await Student.objects.filter(telegram_id=user_id).aexists()
    ):
        return True
    return False


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
delete_handler = CommandHandler("delete_account", delete_account)
