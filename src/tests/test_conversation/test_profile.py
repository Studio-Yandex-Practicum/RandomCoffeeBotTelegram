from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import (
    CHOOSE_ROLE_MESSAGE,
    START_PAIR_SEARCH_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.conversation_handlers import profile
from bot.keyboards.command_keyboards import start_keyboard_markup
from bot.keyboards.conversation_keyboards import role_choice_keyboard_markup


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
        CHOOSE_ROLE_MESSAGE
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        role_choice_keyboard_markup
    )


@pytest.mark.skip(reason="need connection to db")
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
        "profession": "test_prof",
        "name": "test_name",
        "contact": "test_contact",
        "role": "student",
    }
    result = await profile(update, context)
    update.callback_query.edit_message_text.assert_awaited_with(
        START_PAIR_SEARCH_MESSAGE
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        reply_markup=start_keyboard_markup
    )
    assert States.START == result
