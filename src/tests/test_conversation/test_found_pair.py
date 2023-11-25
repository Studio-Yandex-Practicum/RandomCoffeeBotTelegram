from unittest.mock import Mock

import pytest
from bot.handlers.conversation_handlers import found_pair
from bot.constants.states import States


@pytest.mark.asyncio
async def test_found_pair_state(update, context):
    """
    Проверяем, что found_pair handler возвращает
    нужное состояние.
    """
    current_user = Mock()
    found_user = Mock()
    result = await found_pair(update, context, current_user, found_user)
    assert result == States.CALLING_IS_SUCCESSFUL
