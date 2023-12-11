import pytest
from telegram.constants import ParseMode

from bot.utils.db_utils.message import get_message_bot
from bot.handlers.conversation_handlers import next_time


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_next_time_handler(update, context):
    """
    Проверяем, что next_time handler
    возвращает нужное сообщение.
    """
    await next_time(update, context)

    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("next_time_message"),
        parse_mode=ParseMode.HTML,
    )
