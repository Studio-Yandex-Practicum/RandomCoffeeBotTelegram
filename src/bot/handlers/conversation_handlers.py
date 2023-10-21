from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.constants.links import COMMUNICATE_URL
from bot.constants.messages import (
    CHANGE_NAME_MESSAGE,
    CHOOSE_PROFESSION_MESSAGE,
    CHOOSE_ROLE_MESSAGE,
    FOUND_PAIR,
    GUESS_NAME_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
    PROFILE_MESSAGE,
    START_PAIR_SEARCH_MESSAGE,
    USERNAME_NOT_FOUND_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.handlers.schedulers import send_is_pair_successful_message
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import (
    build_profession_keyboard,
    guess_name_keyboard_markup,
    profile_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import Profession, Recruiter, Student
from bot.utils.pagination import parse_callback_data
from bot.utils.pair import make_pair
from core.config.logging import debug_logger


@debug_logger
async def go(update: Update, context: CallbackContext):
    """Обработчик кнопки "GO"."""
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    if not await user_is_exist(user.id):
        await query.edit_message_text(CHOOSE_ROLE_MESSAGE)
        await query.edit_message_reply_markup(role_choice_keyboard_markup)
        return States.ROLE_CHOICE
    else:
        TIME_IN_SECONDS = 50  # для теста сделал задержку в 50 секунд
        context.job_queue.run_once(
            callback=send_is_pair_successful_message,
            when=TIME_IN_SECONDS,
            user_id=user.id,
            data=user,
        )
        await query.message.reply_text(PAIR_SEARCH_MESSAGE)
        return await search_pair(update, context)


async def search_pair(update: Update, context: CallbackContext):
    """Поиск пары."""
    query = update.callback_query
    role = context.user_data["role"]
    model, opposite_model = (
        (Student, Recruiter) if role == "student" else (Recruiter, Student)
    )
    user_has_no_pair = (
        await opposite_model.objects.filter(has_pair=False)
        .exclude(**{f"passedpair__{role}": query.from_user.id})
        .order_by("search_start_time")
        .afirst()
    )
    if user_has_no_pair:
        return await found_pair(update, context, model, user_has_no_pair)
    return ConversationHandler.END


@debug_logger
async def found_pair(
    update: Update, context: CallbackContext, model, user_has_no_pair
):
    """Обработчик найденной пары found_pair."""
    query = update.callback_query
    telegram_id = query.from_user.id
    user = await model.objects.aget(telegram_id=telegram_id)
    profession, student, recruiter = (
        ("It-рекрутер", user, user_has_no_pair)
        if context.user_data["role"] == "student"
        else (user_has_no_pair.profession, user_has_no_pair, user)
    )
    await make_pair(student, recruiter)
    await query.message.reply_text(
        FOUND_PAIR.format(
            user_has_no_pair.name,
            profession,
            user_has_no_pair.telegram_username,
            COMMUNICATE_URL,
        )
    )
    return ConversationHandler.END


@debug_logger
async def next_time(update: Update, context: CallbackContext):
    """Обработчик кнопки "В следующий раз"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(NEXT_TIME_MESSAGE)
    await query.edit_message_reply_markup(reply_markup=restart_keyboard_markup)
    return States.NEXT_TIME


@debug_logger
async def restart_callback(update: Update, context: CallbackContext):
    """Обработчик для кнопки start."""
    query = update.callback_query
    await query.answer()
    return await start(update, context)


@debug_logger
async def role_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора роли."""
    query = update.callback_query
    context.user_data["role"] = query.data
    await send_name_message(update, context)
    return States.SET_NAME


@debug_logger
async def change_name(update: Update, context: CallbackContext):
    """Обработчик для кнопки "Изменить имя"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(CHANGE_NAME_MESSAGE)
    return States.SET_NEW_NAME


@debug_logger
async def set_new_name(update: Update, context: CallbackContext):
    """Обработчик для ввода нового имени."""
    new_name = update.message.text
    context.user_data["name"] = new_name
    await send_name_message(update, context)
    return States.SET_NAME


@debug_logger
async def continue_name(update: Update, context: CallbackContext):
    """Обработчик для кнопки 'Продолжить'."""
    query = update.callback_query
    if context.user_data["role"] == "student":
        page_number = parse_callback_data(query.data)
        await query.answer()
        keyboard = await build_profession_keyboard(page_number)
        if query.message.reply_markup.to_json() != keyboard.markup:
            await query.edit_message_text(CHOOSE_PROFESSION_MESSAGE)
            await query.edit_message_reply_markup(reply_markup=keyboard.markup)
        return States.PROFESSION_CHOICE
    else:
        context.user_data["profession"] = "It-рекрутер"
        return await check_username(update, context)


@debug_logger
async def profession_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора профессии."""
    query = update.callback_query
    profession = await Profession.objects.aget(professional_key=query.data)
    context.user_data["profession"] = profession.name
    return await check_username(update, context)


@debug_logger
async def set_phone_number(update: Update, context: CallbackContext):
    """Обработчик для ввода номера телефона."""
    phone_number = update.message.text
    context.user_data["contact"] = phone_number
    await send_profile_form(update, context)
    return States.PROFILE


@debug_logger
async def profile(update: Update, context: CallbackContext):
    """Обработчик для профиля."""
    query = update.callback_query
    if query.data == "fill_again":
        await query.edit_message_text(CHOOSE_ROLE_MESSAGE)
        await query.edit_message_reply_markup(role_choice_keyboard_markup)
        return States.ROLE_CHOICE
    await to_create_user_in_db(update, context)
    if await user_is_exist(query.from_user.id):
        await query.edit_message_text(START_PAIR_SEARCH_MESSAGE)
        await query.edit_message_reply_markup(
            reply_markup=start_keyboard_markup
        )
        return States.START
    else:
        logger.error(
            f"Пользователь {query.from_user} не сохранен в базе данных."
        )


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


async def check_username(update: Update, context: CallbackContext):
    """Проверяет наличие username."""
    query = update.callback_query
    if not query.from_user.username:
        await query.edit_message_text(USERNAME_NOT_FOUND_MESSAGE)
        return States.SET_PHONE_NUMBER
    await send_profile_form(update, context)
    return States.PROFILE


async def send_profile_form(update: Update, context: CallbackContext):
    """Отправляет форму с именем или телефоном."""
    query = update.callback_query
    profession = context.user_data["profession"]
    name = context.user_data["name"]
    if query:
        context.user_data["contact"] = query.from_user.username
        await query.answer()
        await query.edit_message_text(
            PROFILE_MESSAGE.format(
                name, profession, context.user_data["contact"]
            )
        )
        await query.edit_message_reply_markup(profile_keyboard_markup)
    else:
        await update.message.reply_text(
            PROFILE_MESSAGE.format(
                name, profession, context.user_data["contact"]
            ),
            reply_markup=profile_keyboard_markup,
        )


async def to_create_user_in_db(update: Update, context: CallbackContext):
    """Сохраняет пользователя в базе данных."""
    query = update.callback_query
    user_data = {
        "telegram_id": query.from_user.id,
        "name": context.user_data["name"],
        "surname": query.from_user.last_name,
        "telegram_username": context.user_data["contact"],
    }
    profession = await Profession.objects.aget(
        name=context.user_data["profession"]
    )
    try:
        if context.user_data["role"] == "recruiter":
            await Recruiter.objects.acreate(**user_data)
        else:
            await Student.objects.acreate(profession=profession, **user_data)
    except Exception as error:
        logger.error(f"Не удалось сохранить данные в таблицу: {error}")


async def user_is_exist(user_id: int) -> bool:
    """Проверяет наличие юзера в базе данных."""
    if (
        await Recruiter.objects.filter(telegram_id=user_id).aexists()
        or await Student.objects.filter(telegram_id=user_id).aexists()
    ):
        # Может быть будет иметь смысл возвращать не bool, а объект из БД.
        return True
    return False
