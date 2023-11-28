from unittest.mock import AsyncMock

import pytest

from bot.constants.states import States
from bot.handlers.conversation_handlers import set_phone_number


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_set_phone_number(update, context):
    """
    Тест проверяет, что функция set_phone_number
    правильно обрабатывает сообщение и
    возвращает правильное состояние.
    """
    update.callback_query = None
    update.message = AsyncMock()
    contact = "+7(111)111-11-11"
    update.message.text = contact
    context.user_data = {"profession": "test_prof", "name": "test_name"}

    result = await set_phone_number(update, context)

    assert context.user_data["contact"] == contact
    assert result == States.PROFILE
