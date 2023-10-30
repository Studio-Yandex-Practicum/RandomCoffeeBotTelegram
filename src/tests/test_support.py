from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import ASSISTANCE_MESSAGE
from bot.handlers import command_handlers
from bot.keyboards.command_keyboards import create_support_keyboard


@pytest.mark.asyncio
async def test_support_handler(
    update,
    context,
    mocked_reply_markup,
    db,
):
    """
    Проверяем, что support handler
    возвращает нужное сообщение и нужную клавиатуру.
    """
    update.message = AsyncMock()
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)

    await command_handlers.support_bot(update, context)

    update.message.reply_text.assert_called_with(
        text=ASSISTANCE_MESSAGE,
        reply_markup=await create_support_keyboard(),
    )
