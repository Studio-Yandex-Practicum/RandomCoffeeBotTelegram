from unittest.mock import AsyncMock

import pytest
from bot.handlers.conversation_handlers import search_pair
from bot.constants.states import States

from bot.constants.messages import PAIR_SEARCH_MESSAGE


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_search_pair(update, context):
    """
    Проверяем, что search_pair handler возвращает
    нужное состояние.
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

    result = await search_pair(update, context)

    assert result == States.CALLING_IS_SUCCESSFUL
    query.message.reply_text.assert_called_with(PAIR_SEARCH_MESSAGE)
