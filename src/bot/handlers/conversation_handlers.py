from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.constants.messages import (
    CHANGE_NAME_MESSAGE,
    CHOOSE_PROFESSION_MESSAGE,
    CHOOSE_ROLE_MESSAGE,
    GUESS_NAME_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
    PROFILE_MESSAGE,
    USERNAME_NOT_FOUND_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.keyboards.conversation_keyboards import (
    guess_name_keyboard_markup,
    profession_choice_keyboard_markup,
    profile_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import Recruiter, Student
from core.config.logging import log_handler


@log_handler
async def go(update: Update, context: CallbackContext):
    """Обработчик кнопки "GO"."""
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    if not (
        await Recruiter.objects.filter(telegram_id=user.id).aexists()
        or await Student.objects.filter(telegram_id=user.id).aexists()
    ):
        await query.edit_message_text(CHOOSE_ROLE_MESSAGE)
        await query.edit_message_reply_markup(role_choice_keyboard_markup)
        return States.ROLE_CHOICE
    else:
        await query.message.reply_text(PAIR_SEARCH_MESSAGE)
        return ConversationHandler.END  # Тут будет States.PAIR_SEARCH


@log_handler
async def next_time(update: Update, context: CallbackContext):
    """Обработчик кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(NEXT_TIME_MESSAGE)
    await query.edit_message_reply_markup(reply_markup=restart_keyboard_markup)
    return States.NEXT_TIME


@log_handler
async def restart_callback(update: Update, context: CallbackContext):
    """Обработчик для кнопки start."""
    query = update.callback_query
    await query.answer()
    return await start(update, context)


@log_handler
async def role_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора роли."""
    query = update.callback_query
    context.user_data["role"] = query.data
    await send_name_message(update, context)
    return States.SET_NAME


@log_handler
async def change_name(update: Update, context: CallbackContext):
    """Обработчик для кнопки "Изменить имя"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(CHANGE_NAME_MESSAGE)
    return States.SET_NEW_NAME


@log_handler
async def set_new_name(update: Update, context: CallbackContext):
    """Обработчик для ввода нового имени."""
    new_name = update.message.text
    context.user_data["name"] = new_name
    await send_name_message(update, context)
    return States.SET_NAME


@log_handler
async def continue_name(update: Update, context: CallbackContext):
    """Обработчик для кнопки 'Продолжить'."""
    query = update.callback_query
    if context.user_data["role"] == "student":
        await query.edit_message_text(CHOOSE_PROFESSION_MESSAGE)
        await query.edit_message_reply_markup(
            profession_choice_keyboard_markup
        )
        return States.PROFESSION_CHOICE
    else:
        query = update.callback_query
        username = query.from_user.username
        context.user_data["profession"] = "It-рекрутер"
        if not username:
            await query.edit_message_text(USERNAME_NOT_FOUND_MESSAGE)
            return States.SET_PHONE_NUMBER
        await send_profile_form(update, context)
        return States.PROFILE


@log_handler
async def profession_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора профессии."""
    query = update.callback_query
    context.user_data["profession"] = query.data.title()
    username = query.from_user.username
    if not username:
        await query.edit_message_text(USERNAME_NOT_FOUND_MESSAGE)
        return States.SET_PHONE_NUMBER
    await send_profile_form(update, context)
    return States.PROFILE


@log_handler
async def set_phone_number(update: Update, context: CallbackContext):
    """Обработчик для ввода номера телефона."""
    phone_number = update.message.text
    context.user_data["phone"] = phone_number
    await send_profile_form(update, context)
    return States.PROFILE


@log_handler
async def profile(update: Update, context: CallbackContext):
    """Обработчик для профиля."""
    query = update.callback_query
    if query.data == "fill_again":
        await query.edit_message_text(CHOOSE_ROLE_MESSAGE)
        await query.edit_message_reply_markup(role_choice_keyboard_markup)
        return States.ROLE_CHOICE
    else:
        # передать данные в базу данных
        pass
    return ConversationHandler.END


async def send_name_message(update: Update, context: CallbackContext):
    """Отправляет сообщение с именем."""
    query = update.callback_query
    guessed_name = context.user_data.get(
        "name", query.from_user.first_name if query else "unknown"
    )
    if query:
        context.user_data["name"] = guessed_name
        await query.answer()
        await query.edit_message_text(GUESS_NAME_MESSAGE.format(guessed_name))
        await query.edit_message_reply_markup(guess_name_keyboard_markup)
    else:
        await update.message.reply_text(
            GUESS_NAME_MESSAGE.format(guessed_name),
            reply_markup=guess_name_keyboard_markup,
        )


# async def check_username(update: Update, context: CallbackContext):
#     """"""
#     query = update.callback_query
#     username = query.from_user.username
#     username = ''
#     if not username:
#         await query.edit_message_text(USERNAME_NOT_FOUND_MESSAGE)
#         return States.SET_PHONE_NUMBER


async def send_profile_form(update: Update, context: CallbackContext):
    """Отправляет форму с именем или телефоном."""
    query = update.callback_query
    profession = context.user_data["profession"]
    name = context.user_data["name"]
    if query:
        contact = query.from_user.username
        await query.answer()
        await query.edit_message_text(
            PROFILE_MESSAGE.format(name, profession, contact)
        )
        await query.edit_message_reply_markup(profile_keyboard_markup)
    else:
        contact = context.user_data["phone"]
        await update.message.reply_text(
            PROFILE_MESSAGE.format(name, profession, contact),
            reply_markup=profile_keyboard_markup,
        )
