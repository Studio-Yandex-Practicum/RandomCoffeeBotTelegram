from unittest.mock import AsyncMock

import pytest
from telegram.constants import ParseMode

from bot.utils.db_utils.message import get_message_bot
from bot.handlers import command_handlers
from bot.keyboards.command_keyboards import start_keyboard_markup


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_start_handler_answer_to_user_message(
    update,
    context,
    mocked_reply_markup,
):
    """
    Проверяем, что start handler
    возвращает нужное сообщение и нужную клавиатуру.
    """
    update.message = AsyncMock()
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)

    await command_handlers.start(update, context)

    update.message.reply_text.assert_called_with(
        text=await get_message_bot("start_message"),
        reply_markup=start_keyboard_markup,
        parse_mode=ParseMode.HTML,
    )
