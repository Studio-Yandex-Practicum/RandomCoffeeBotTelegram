from unittest.mock import AsyncMock

import pytest
from telegram.constants import ParseMode

from bot.utils.db_utils.message import get_message_bot
from bot.handlers import command_handlers
from bot.keyboards.command_keyboards import create_support_keyboard


@pytest.mark.asyncio
async def test_redirection_to_support_handler(
    update,
    context,
    mocked_reply_markup,
    db,
):
    """
    Проверяем, что redirection_to_support handler
    возвращает нужное сообщение и нужную клавиатуру.
    """
    update.callback_query = AsyncMock()
    update.callback_query.data = "support"
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)

    await command_handlers.redirection_to_support(update, context)
    update.callback_query.edit_message_text.assert_called_with(
        text=await get_message_bot("assistance_message"),
        reply_markup=await create_support_keyboard(),
        parse_mode=ParseMode.HTML,
    )
