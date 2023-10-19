import asyncio

from asgiref.sync import sync_to_async
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
    IS_PAIR_SUCCESSFUL_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
    PROFILE_MESSAGE,
    START_PAIR_SEARCH_MESSAGE,
    USERNAME_NOT_FOUND_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import (
    guess_name_keyboard_markup,
    is_pair_successful_keyboard_markup,
    profession_choice_keyboard_markup,
    profile_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import Profession, Recruiter, Student
from bot.utils.pair import make_pair
from core.config.logging import log_handler


@log_handler
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
        TIME_IN_SECONDS = 50  # для теста сделал задержку в 10 секунд
        context.job_queue.run_once(
            callback=send_is_pair_successful_message,
            when=TIME_IN_SECONDS,
            user_id=user.id,
        )
        return await search_pair(update, context)


async def search_pair(update: Update, context: CallbackContext):
    """Поиск пары."""
    query = update.callback_query
    telegram_id = query.from_user["id"]
    if context.user_data["role"] == "student":
        users_has_no_pair = await sync_to_async(list)(
            Recruiter.objects.filter(has_pair=False).exclude(
                passedpair__student=telegram_id
            )
        )
    else:
        users_has_no_pair = await sync_to_async(list)(
            Student.objects.filter(has_pair=False).exclude(
                passedpair__recruiter=telegram_id
            )
        )

    if users_has_no_pair:
        user_has_no_pair = users_has_no_pair[0]
        if context.user_data["role"] == "student":
            profession = "It-рекрутер"
            await make_pair(
                await Student.objects.aget(telegram_id=telegram_id),
                user_has_no_pair,
            )
        else:
            profession = user_has_no_pair.profession
            await make_pair(
                user_has_no_pair,
                await Recruiter.objects.aget(telegram_id=telegram_id),
            )
        await query.message.reply_text(
            FOUND_PAIR.format(
                user_has_no_pair.name,
                profession,
                context.user_data["profession"],
                user_has_no_pair.telegram_username,
                COMMUNICATE_URL,
            )
        )
        return ConversationHandler.END
    TIME_WAIT_BEFORE_REQUESTS = 5
    await query.message.reply_text(PAIR_SEARCH_MESSAGE)
    await asyncio.sleep(TIME_WAIT_BEFORE_REQUESTS)
    return await search_pair(update, context)


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
        context.user_data["profession"] = "It-рекрутер"
        return await check_username(update, context)


@log_handler
async def profession_choice(update: Update, context: CallbackContext):
    """Обработчик для выбора профессии."""
    query = update.callback_query
    context.user_data["profession"] = query.data.title()
    return await check_username(update, context)


@log_handler
async def set_phone_number(update: Update, context: CallbackContext):
    """Обработчик для ввода номера телефона."""
    phone_number = update.message.text
    context.user_data["contact"] = phone_number
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


async def send_is_pair_successful_message(context: CallbackContext):
    """Отправляет сообщение состоялся ли звонок."""
    await context.bot.send_message(
        chat_id=context.job.user_id,
        text=IS_PAIR_SUCCESSFUL_MESSAGE,
        reply_markup=is_pair_successful_keyboard_markup,
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
    profession = context.user_data["profession"]
    user_data = {
        "telegram_id": query.from_user.id,
        "name": context.user_data["name"],
        "surname": query.from_user.last_name,
        "telegram_username": context.user_data["contact"],
    }
    profession, created = await Profession.objects.aget_or_create(
        name=profession
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
