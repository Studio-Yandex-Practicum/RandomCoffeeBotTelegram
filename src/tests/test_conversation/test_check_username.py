from unittest.mock import AsyncMock

import pytest

from bot.constants.states import States
from bot.handlers.conversation_handlers import check_username


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_check_username_with_username(update, context):
    """
    Проверяем, что check_username
    возвращает правильное состояние
    если у пользователя есть username.
    """
    update.callback_query = AsyncMock()
    update.callback_query.from_user.username = "test_username"

    state = await check_username(update, context)

    assert state == States.PROFILE


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_check_username_without_username(update, context):
    """
    Проверяем, что check_username
    возвращает правильное состояние
    если у пользователя нет username.
    """
    update.callback_query = AsyncMock()
    update.callback_query.from_user.username = ""

    state = await check_username(update, context)

    assert state == States.SET_PHONE_NUMBER
