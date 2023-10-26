import pytest

from bot.constants.states import States
from bot.handlers.conversation_handlers import set_new_name


@pytest.mark.asyncio
async def test_set_new_name(
    update, context, mocked_message, mocked_message_text
):
    """
    Функция set_new_name корректно устанавливает новое имя пользователя в
    context,user_data и возвращает правильное состояние.
    """
    update.message = mocked_message
    context.user_data = {}

    result = await set_new_name(update, context)

    assert context.user_data["name"] == mocked_message_text
    assert result == States.SET_NAME
