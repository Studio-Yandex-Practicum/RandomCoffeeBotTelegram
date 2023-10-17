from unittest.mock import AsyncMock

import pytest

from bot.constants.states import States
from bot.handlers.conversation_handlers import role_choice


@pytest.mark.asyncio
async def test_role_choice(update, context):
    """
    Тест проверяет, что функция role_choice
    возвращает правильное состояние.
    """
    update.callback_query = AsyncMock()

    result = await role_choice(update, context)

    assert result == States.SET_NAME
