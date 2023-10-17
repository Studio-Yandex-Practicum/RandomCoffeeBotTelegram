import pytest

from bot.constants.messages import NEXT_TIME_MESSAGE
from bot.handlers.conversation_handlers import next_time


@pytest.mark.asyncio
async def test_next_time_handler(update, context):
    """
    Проверяем, что next_time handler
    возвращает нужное сообщение.
    """
    await next_time(update, context)

    update.callback_query.edit_message_text.assert_awaited_with(
        NEXT_TIME_MESSAGE
    )
