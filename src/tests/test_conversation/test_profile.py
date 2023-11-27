from unittest.mock import AsyncMock

import pytest

from bot.utils.db_utils.message import get_message_bot
from bot.constants.states import States
from bot.handlers.conversation_handlers import profile
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import role_choice_keyboard_markup


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_profile_fill_again(update, context):
    """
    Проверяем, что profile handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователя выбрал заполнить данные заново.
    """
    query = update.callback_query = AsyncMock()
    query.data = "fill_again"

    result = await profile(update, context)

    assert States.ROLE_CHOICE == result

    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("choose_role_message")
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        role_choice_keyboard_markup
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_profile_create_user(update, context):
    """
    Проверяем, что profile handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователя нажал "Все верно".
    """
    update.callback_query = AsyncMock()
    query = update.callback_query
    query.from_user.id = 321
    query.from_user.last_name = "test_surname"
    context.user_data = {
        "profession": "prof-1",
        "name": "test_name",
        "contact": "test_contact",
        "role": "itspecialist",
    }
    result = await profile(update, context)
    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("start_pair_search_message")
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        reply_markup=start_keyboard_markup
    )
    assert States.START == result
