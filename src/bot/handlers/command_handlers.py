from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from bot.constants.messages import (
    HELP_MESSAGE,
    NEXT_TIME_MESSAGE
    ASSISTANCE_MESSAGE,
    START_MESSAGE,
)
from bot.keyboards.command_keyboards import (
    help_keyboard_markup,
    next_time_keyboard_markup,
    start_keyboard_markup,
    support_keyboard_markup,
)
from core.config.logging import log_handler


@log_handler
async def start(update: Update, context: CallbackContext) -> None:
    """Функция-обработчик команды start."""
    if update.message is not None:
        await update.message.reply_text(
            text=START_MESSAGE, reply_markup=start_keyboard_markup
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
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


async def start_return(update: Update, context: CallbackContext):
    """Функция-обработчик для кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    return await start(update, context)


async def next_time(update: Update, context: CallbackContext):
    """Функция-обработчик для кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(
        NEXT_TIME_MESSAGE, reply_markup=next_time_keyboard_markup
    )
    
    
async def redirection_to_support(
    update: Update, context: CallbackContext
) -> None:
    """Перенаправление на команду /support."""
    query = update.callback_query
    if query.data == "support":
        await query.edit_message_text(
            text=ASSISTANCE_MESSAGE, reply_markup=support_keyboard_markup
        )


start_handler = CommandHandler("start", start)
support_bot_handler = CommandHandler("support", support_bot)
help_handler = CommandHandler("help", help)
next_time_query_handler = CallbackQueryHandler(
    next_time, pattern="^next_time$"
)
start_return_query_handler = CallbackQueryHandler(
    start_return, pattern="^start_return$"
)
redirection_to_support_handler = CallbackQueryHandler(redirection_to_support)
