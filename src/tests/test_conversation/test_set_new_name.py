import pytest

from bot.handlers.conversation_handlers import set_new_name
from bot.constants.states import States


@pytest.mark.asyncio
async def test_set_new_name(
    update, context, mocked_message, mocked_message_text
):
    update.message = mocked_message
    context.user_data = {}

    result = await set_new_name(update, context)

    assert context.user_data["name"] == mocked_message_text
    assert result == States.SET_NAME
