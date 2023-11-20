from typing import Union

from django.utils import timezone
from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from bot.constants.links import FORM_KEYS
from bot.constants.messages import (
    CHANGE_NAME_MESSAGE,
    CHOOSE_PROFESSION_MESSAGE,
    CHOOSE_ROLE_MESSAGE,
    FOUND_PAIR,
    GUESS_NAME_MESSAGE,
    NEXT_TIME_MESSAGE,
    PAIR_SEARCH_MESSAGE,
    POST_CALL_MESSAGE,
    POST_CALL_MESSAGE_FOR_IT_SPECIALIST,
    POST_CALL_MESSAGE_FOR_RECRUITER,
    PROFILE_MESSAGE,
    START_PAIR_SEARCH_MESSAGE,
    USERNAME_NOT_FOUND_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import (
    build_profession_keyboard,
    guess_name_keyboard_markup,
    profile_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import CreatedPair, ItSpecialist, Profession, Recruiter
from bot.utils.form_url import get_form_url
from bot.utils.message_senders import send_is_pair_successful_message
from bot.utils.pagination import parse_callback_data
from bot.utils.pair import delete_pair, make_pair
from core.config.logging import debug_logger

TIME_IN_SECONDS = (
    5  # Время, через которое происходит оповещение о состоявщемся интервью
)


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
        return await search_pair(update, context)


async def search_pair(update: Update, context: CallbackContext):
    """Поиск пары."""
    query = update.callback_query
    role = context.user_data["role"]
    telegram_id = query.from_user.id
    model, opposite_model = (
        (ItSpecialist, Recruiter)
        if role == "itspecialist"
        else (Recruiter, ItSpecialist)
    )
    current_user = await model.objects.aget(telegram_id=telegram_id)
    current_user.search_start_time = timezone.now()
    await current_user.asave(update_fields=("search_start_time",))
    found_user = (
        await opposite_model.objects.filter(has_pair=False)
        .exclude(**{f"passedpair__{role}": telegram_id})
        .order_by("search_start_time")
        .afirst()
    )
    if found_user:
        return await found_pair(update, context, current_user, found_user)
    await query.message.reply_text(PAIR_SEARCH_MESSAGE)
    return States.CALLING_IS_SUCCESSFUL


@debug_logger
async def found_pair(
    update: Update, context: CallbackContext, current_user, found_user
):
    """Обработчик найденной пары found_pair."""
    itspecialist, recruiter = (
        (current_user, found_user)
        if context.user_data["role"] == "itspecialist"
        else (found_user, current_user)
    )
    if await make_pair(itspecialist, recruiter):
        context.job_queue.run_once(
            callback=send_is_pair_successful_message,
            when=TIME_IN_SECONDS,
            user_id=itspecialist.telegram_id,
        )
        context.job_queue.run_once(
            callback=send_is_pair_successful_message,
            when=TIME_IN_SECONDS,
            user_id=recruiter.telegram_id,
        )
        await send_both_users_message(update, context, itspecialist, recruiter)
    return States.CALLING_IS_SUCCESSFUL


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
    if context.user_data["role"] == "itspecialist":
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


async def send_both_users_message(
    update: Update, context: CallbackContext, itspecialist, recruiter
):
    """Возвращает обоим пользователям информацию об их найденой паре."""
    guide_url = await get_form_url(FORM_KEYS["GUIDE"])
    itspecialist_profession = await Profession.objects.aget(
        pk=itspecialist.profession_id
    )
    await context.bot.send_message(
        chat_id=itspecialist.telegram_id,
        text=FOUND_PAIR.format(
            recruiter.name,
            "It-рекрутер",
            recruiter.telegram_username,
            guide_url,
        ),
    )
    await context.bot.send_message(
        chat_id=recruiter.telegram_id,
        text=FOUND_PAIR.format(
            itspecialist.name,
            itspecialist_profession,
            itspecialist.telegram_username,
            guide_url,
        ),
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
    try:
        if context.user_data["role"] == "recruiter":
            await Recruiter.objects.acreate(**user_data)
        else:
            profession = await Profession.objects.aget(
                name=context.user_data["profession"]
            )
            await ItSpecialist.objects.acreate(
                profession=profession, **user_data
            )
    except Exception as error:
        logger.error(f"Не удалось сохранить данные в таблицу: {error}")


async def user_is_exist(user_id: int) -> bool:
    """Проверяет наличие юзера в базе данных."""
    if (
        await Recruiter.objects.filter(telegram_id=user_id).aexists()
        or await ItSpecialist.objects.filter(telegram_id=user_id).aexists()
    ):
        return True
    return False


async def get_active_pair(role: str, user_id: int) -> Union[CreatedPair, None]:
    """Возвращает активную пару, с участием пользователя."""
    if role == "itspecialist":
        return (
            await CreatedPair.objects.filter(itspecialist=user_id)
            .select_related("itspecialist", "recruiter")
            .afirst()
        )
    else:
        return (
            await CreatedPair.objects.filter(recruiter=user_id)
            .select_related("itspecialist", "recruiter")
            .afirst()
        )


@debug_logger
async def calling_is_successful(update: Update, context: CallbackContext):
    """Возвращает пользователям сообщение об обратной связи."""
    query = update.callback_query
    current_user = query.from_user
    feedback_url = await get_form_url(FORM_KEYS["FEEDBACK"])
    pair = await get_active_pair(context.user_data["role"], current_user.id)
    await query.answer()
    if pair:
        await delete_pair(
            pair.itspecialist, pair.recruiter, query.data == "yes"
        )
    if query.data == "no":
        communicate_url = await get_form_url(FORM_KEYS["FEEDBACK"])
        await query.edit_message_text(
            POST_CALL_MESSAGE.format(communicate_url)
        )
    elif context.user_data["role"] == "recruiter":
        await query.edit_message_text(
            POST_CALL_MESSAGE_FOR_RECRUITER.format(feedback_url)
        )
    else:
        await query.edit_message_text(POST_CALL_MESSAGE_FOR_IT_SPECIALIST)
    await query.edit_message_reply_markup(reply_markup=start_keyboard_markup)
    return States.START
