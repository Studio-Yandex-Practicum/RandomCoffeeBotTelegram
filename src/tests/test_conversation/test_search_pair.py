from unittest.mock import AsyncMock

import pytest
from telegram.constants import ParseMode

from bot.handlers.conversation_handlers import search_pair
from bot.utils.db_utils.message import get_message_bot
from bot.constants.states import States

from bot.keyboards.conversation_keyboards import (
    cancel_pair_search_keyboard_markup,
)


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

    assert result == States.CANCEL
    query.message.reply_text.assert_called_with(
        await get_message_bot("pair_search_message"),
        reply_markup=cancel_pair_search_keyboard_markup,
        parse_mode=ParseMode.HTML,
    )
