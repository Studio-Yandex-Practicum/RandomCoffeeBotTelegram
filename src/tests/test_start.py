from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import START_MESSAGE
from bot.handlers import command_handlers
from bot.keyboards.command_keyboards import start_keyboard_markup


@pytest.mark.asyncio
async def test_start_handler_answer_to_user_message(
    update,
    context,
    mocked_reply_markup,
):
    """Проверяем, что start handler, возвращает нужное сообщение и нужную клавиатуру."""
    update.message = AsyncMock()
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)

    await command_handlers.start(update, context)

    update.message.reply_text.assert_called_with(
        text=START_MESSAGE,
        reply_markup=start_keyboard_markup,
    )
