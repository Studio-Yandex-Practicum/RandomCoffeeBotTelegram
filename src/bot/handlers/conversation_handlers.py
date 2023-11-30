from typing import Literal, Optional, Union

from django.utils import timezone
from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from bot.constants.links import FORM_KEYS
from bot.constants.states import States
from bot.handlers.command_handlers import start
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import (
    build_profession_keyboard,
    cancel_pair_search_keyboard_markup,
    profile_keyboard_markup,
    restart_keyboard_markup,
    role_choice_keyboard_markup,
)
from bot.models import ItSpecialist, Profession, Recruiter
from bot.utils.db_utils.message import get_message_bot
from bot.utils.db_utils.pair import delete_pair, get_active_pair, make_pair
from bot.utils.db_utils.user import (
    deleting_account,
    to_create_user_in_db,
    user_is_exist,
)
from bot.utils.form_url import get_form_url
from bot.utils.message_senders import (
    send_is_pair_successful_message,
    send_name_message,
)
from bot.utils.pagination import parse_callback_data
from bot.utils.validate_phone import validation_phone_number
from core.config.logging import debug_logger

TIME_IN_SECONDS = (
    5  # Время, через которое происходит оповещение о состоявщемся интервью
)


@debug_logger
async def go(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "GO"."""
    query = update.callback_query
    if query:
        user = query.from_user
        await query.answer()
        await query.edit_message_reply_markup(reply_markup=None)
        if not await user_is_exist(user.id):
            await query.edit_message_text(
                await get_message_bot("choose_role_message")
            )
            await query.edit_message_reply_markup(role_choice_keyboard_markup)
            return States.ROLE_CHOICE
        else:
            return await search_pair(update, context)
    return None


async def search_pair(
    update: Update, context: CallbackContext
) -> Literal[States.CANCEL]:
    """Поиск пары."""
    query = update.callback_query
    if query and context.user_data and query.message:
        role = context.user_data["role"]
        telegram_id = query.from_user.id
        model, opposite_model = (
            (ItSpecialist, Recruiter)
            if role == "itspecialist"
            else (Recruiter, ItSpecialist)
        )
        current_user = await model.objects.aget(telegram_id=telegram_id)
        current_user.search_start_time = timezone.now()
        current_user.in_search_pair = True
        await current_user.asave(
            update_fields=("search_start_time", "in_search_pair")
        )
        found_user = (
            await opposite_model.objects.filter(
                has_pair=False, in_search_pair=True
            )
            .exclude(**{f"passedpair__{role}": telegram_id})
            .order_by("search_start_time")
            .afirst()
        )
        if found_user:
            return await found_pair(update, context, current_user, found_user)
        await query.message.reply_text(
            await get_message_bot("pair_search_message"),
            reply_markup=cancel_pair_search_keyboard_markup,
        )
    return States.CANCEL


@debug_logger
async def found_pair(
    update: Update,
    context: CallbackContext,
    current_user: Union[Recruiter, ItSpecialist],
    found_user: Union[Recruiter, ItSpecialist],
) -> Literal[States.CALLING_IS_SUCCESSFUL]:
    """Обработчик найденной пары found_pair."""
    if context.user_data and context.job_queue:
        itspecialist, recruiter = (
            (current_user, found_user)
            if context.user_data["role"] == "itspecialist"
            else (found_user, current_user)
        )
        if await make_pair(itspecialist, recruiter):
            context.job_queue.run_once(  # type: ignore[attr-defined]
                callback=send_is_pair_successful_message,
                when=TIME_IN_SECONDS,
                user_id=itspecialist.telegram_id,
            )
            context.job_queue.run_once(  # type: ignore[attr-defined]
                callback=send_is_pair_successful_message,
                when=TIME_IN_SECONDS,
                user_id=recruiter.telegram_id,
            )
            await send_both_users_message(
                update, context, itspecialist, recruiter
            )
    return States.CALLING_IS_SUCCESSFUL


@debug_logger
async def next_time(
    update: Update, context: CallbackContext
) -> Literal[States.NEXT_TIME]:
    """Обработчик кнопки "В следующий раз"."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            await get_message_bot("next_time_message")
        )
        await query.edit_message_reply_markup(
            reply_markup=restart_keyboard_markup
        )
    return States.NEXT_TIME


@debug_logger
async def restart_callback(
    update: Update, context: CallbackContext
) -> Literal[States.START]:
    """Обработчик для кнопки start."""
    query = update.callback_query
    if query:
        await query.answer()
    return await start(update, context)


@debug_logger
async def role_choice(
    update: Update, context: CallbackContext
) -> Literal[States.SET_NAME]:
    """Обработчик для выбора роли."""
    query = update.callback_query
    context.user_data["role"] = query.data
    await send_name_message(update, context)
    return States.SET_NAME


@debug_logger
async def change_name(
    update: Update, context: CallbackContext
) -> Literal[States.SET_NEW_NAME]:
    """Обработчик для кнопки "Изменить имя"."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(await get_message_bot("change_name_message"))
    return States.SET_NEW_NAME


@debug_logger
async def set_new_name(
    update: Update, context: CallbackContext
) -> Literal[States.SET_NAME]:
    """Обработчик для ввода нового имени."""
    context.user_data["name"] = update.message.text
    await send_name_message(update, context)
    return States.SET_NAME


@debug_logger
async def continue_name(
    update: Update, context: CallbackContext
) -> Optional[
    Literal[States.PROFESSION_CHOICE, States.PROFILE, States.SET_PHONE_NUMBER]
]:
    """Обработчик для кнопки 'Продолжить'."""
    query = update.callback_query
    if context.user_data["role"] == "itspecialist":
        page_number = parse_callback_data(query.data)
        await query.answer()
        keyboard = await build_profession_keyboard(page_number)
        if query.message.reply_markup.to_json() != keyboard.markup:
            await query.edit_message_text(
                await get_message_bot("choose_profession_message")
            )
            await query.edit_message_reply_markup(reply_markup=keyboard.markup)
        return States.PROFESSION_CHOICE
    else:
        context.user_data["profession"] = "It-рекрутер"
        return await check_username(update, context)


@debug_logger
async def profession_choice(
    update: Update, context: CallbackContext
) -> Optional[Literal[States.PROFILE, States.SET_PHONE_NUMBER]]:
    """Обработчик для выбора профессии."""
    query = update.callback_query
    profession = await Profession.objects.aget(professional_key=query.data)
    context.user_data["profession"] = profession.name
    return await check_username(update, context)


@debug_logger
async def set_phone_number(
    update: Update, context: CallbackContext
) -> Literal[States.SET_PHONE_NUMBER, States.PROFILE]:
    """Обработчик для ввода номера телефона."""
    if update.message and update.message.text and context.user_data:
        phone_number = update.message.text
        if not await validation_phone_number(phone_number):
            await update.message.reply_text(
                await get_message_bot("message_incorrect_phone_number")
            )
            return States.SET_PHONE_NUMBER
        context.user_data["contact"] = phone_number
        await send_profile_form(update, context)
    return States.PROFILE


@debug_logger
async def profile(
    update: Update, context: CallbackContext
) -> Optional[Literal[States.ROLE_CHOICE, States.START]]:
    """Обработчик для профиля."""
    query = update.callback_query
    if query:
        if query.data == "fill_again":
            await query.edit_message_text(
                await get_message_bot("choose_role_message")
            )
            await query.edit_message_reply_markup(role_choice_keyboard_markup)
            return States.ROLE_CHOICE
        await to_create_user_in_db(update, context)
        if await user_is_exist(query.from_user.id):
            await query.edit_message_text(
                await get_message_bot("start_pair_search_message")
            )
            await query.edit_message_reply_markup(
                reply_markup=start_keyboard_markup
            )
            return States.START
        else:
            logger.error(
                f"Пользователь {query.from_user} не сохранен в базе данных."
            )
    return None


async def check_username(
    update: Update, context: CallbackContext
) -> Optional[Literal[States.PROFILE, States.SET_PHONE_NUMBER]]:
    """Проверяет наличие username."""
    query = update.callback_query
    if query:
        if not query.from_user.username:
            await query.edit_message_text(
                await get_message_bot("username_not_found_message")
            )
            return States.SET_PHONE_NUMBER
        await send_profile_form(update, context)
        return States.PROFILE
    return None


async def send_profile_form(update: Update, context: CallbackContext) -> None:
    """Отправляет форму с именем или телефоном."""
    query = update.callback_query
    if context.user_data:
        profession = context.user_data["profession"]
        name = context.user_data["name"]
    if query:
        context.user_data["contact"] = query.from_user.username
        await query.answer()
        message = await get_message_bot("profile_message")
        await query.edit_message_text(
            message.format(name, profession, context.user_data["contact"])
        )
        await query.edit_message_reply_markup(profile_keyboard_markup)
    elif not query and update.message:
        message = await get_message_bot("profile_message_no_username")
        await update.message.reply_text(
            message.format(name, profession, context.user_data["contact"]),
            reply_markup=profile_keyboard_markup,
        )


async def send_both_users_message(
    update: Update, context: CallbackContext, itspecialist, recruiter
) -> None:
    """Возвращает обоим пользователям информацию об их найденой паре."""
    guide_url = await get_form_url(FORM_KEYS["GUIDE"])
    itspecialist_profession = await Profession.objects.aget(
        pk=itspecialist.profession_id
    )
    found_pair = await get_message_bot("found_pair")
    found_pair_no_username = await get_message_bot("found_pair_no_username")
    form_itspecialist = [found_pair, found_pair_no_username][
        await validation_phone_number(itspecialist.telegram_username)
    ]
    form_recruiter = [found_pair, found_pair_no_username][
        await validation_phone_number(recruiter.telegram_username)
    ]
    await context.bot.send_message(
        chat_id=itspecialist.telegram_id,
        text=form_recruiter.format(
            recruiter.name,
            "It-рекрутер",
            recruiter.telegram_username,
            guide_url,
        ),
    )
    await context.bot.send_message(
        chat_id=recruiter.telegram_id,
        text=form_itspecialist.format(
            itspecialist.name,
            itspecialist_profession,
            itspecialist.telegram_username,
            guide_url,
        ),
    )


async def confirm_delete_account(
    update: Update, context: CallbackContext
) -> Optional[Literal[States.ACCOUNT_DELETED]]:
    """Удаляет пользователя."""
    query = update.callback_query
    if query:
        user_id = query.from_user.id
        await deleting_account(user_id)
        await query.answer()
        await query.edit_message_reply_markup(reply_markup=None)
        await query.edit_message_text(
            await get_message_bot("account_deleted_message")
        )
        await query.edit_message_reply_markup(restart_keyboard_markup)
        return States.ACCOUNT_DELETED
    return None


@debug_logger
async def calling_is_successful(
    update: Update, context: CallbackContext
) -> Literal[States.START]:
    """Возвращает пользователям сообщение об обратной связи."""
    query = update.callback_query
    feedback_url = await get_form_url(FORM_KEYS["FEEDBACK"])
    pair = await get_active_pair(context.user_data["role"], query.from_user.id)
    await query.answer()
    if pair:
        await delete_pair(
            pair.itspecialist, pair.recruiter, query.data == "yes"
        )
    if query.data == "no":
        communicate_url = await get_form_url(FORM_KEYS["FEEDBACK"])
        message = await get_message_bot("post_call_message")
        await query.edit_message_text(message.format(communicate_url))
    elif context.user_data["role"] == "recruiter":
        message = await get_message_bot("post_call_message_for_recruiter")
        await query.edit_message_text(message.format(feedback_url))
    else:
        await query.edit_message_text(
            await get_message_bot("post_call_message_for_it_specialist")
        )
    await query.edit_message_reply_markup(reply_markup=start_keyboard_markup)
    return States.START


async def cancel_pair_search(
    update: Update, context: CallbackContext
) -> Optional[Literal[States.NEXT_TIME]]:
    """Отмена поиска."""
    query = update.callback_query
    if query and context.user_data:
        role = context.user_data["role"]
        telegram_id = query.from_user.id
        model = ItSpecialist if role == "itspecialist" else Recruiter
        current_user = await model.objects.aget(telegram_id=telegram_id)
        current_user.in_search_pair = False
        current_user.search_start_time = None
        await current_user.asave(
            update_fields=("in_search_pair", "search_start_time")
        )
        return await next_time(update, context)
    return None
