from unittest.mock import AsyncMock

import pytest

from bot.handlers.conversation_handlers import change_name
from bot.utils.db_utils.message import get_message_bot
from bot.constants.states import States


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_change_name(update, context):
    """
    Тест проверяет, что функция change_name корректно обрабатывает
    callback_query, изменяет текст сообщения и переводит состояние в
    States.SET_NEW_NAME.
    """
    update.callback_query = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    update.callback_query.answer = AsyncMock()

    result = await change_name(update, context)
    update.callback_query.answer.assert_awaited_once()
    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("change_name_message")
    )
    assert result == States.SET_NEW_NAME
