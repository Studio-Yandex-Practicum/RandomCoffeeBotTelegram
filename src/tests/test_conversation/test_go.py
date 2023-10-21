from unittest.mock import AsyncMock

import pytest
from telegram.ext import ConversationHandler

from bot.constants.messages import (
    CHOOSE_ROLE_MESSAGE,
    PAIR_SEARCH_MESSAGE,
    FOUND_PAIR,
)
from bot.constants.states import States
from bot.handlers.conversation_handlers import go
from bot.keyboards.conversation_keyboards import role_choice_keyboard_markup


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_go_user_is_no_exist(update, context):
    """
    Проверяем, что go handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователя не существует.
    """
    update.callback_query = AsyncMock()
    update.callback_query.from_user.id = 123
    result = await go(update, context)

    assert States.ROLE_CHOICE == result
    update.callback_query.edit_message_text.assert_awaited_with(
        CHOOSE_ROLE_MESSAGE
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        role_choice_keyboard_markup
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_go_user_is_exist(update, context, student):
    """
    Проверяем, что go handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователь существует и пара отсутствует.
    """
    update.callback_query = AsyncMock()
    student = await student
    context.user_data = {"role": "student"}
    update.callback_query.from_user.id = student.telegram_id
    result = await go(update, context)
    update.callback_query.message.reply_text.assert_awaited_with(
        PAIR_SEARCH_MESSAGE
    )
    assert ConversationHandler.END == result
