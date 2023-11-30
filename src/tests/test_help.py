from unittest.mock import AsyncMock

import pytest

from bot.utils.db_utils.message import get_message_bot
from bot.handlers import command_handlers
from bot.keyboards.command_keyboards import help_keyboard_markup


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_help_handler(
    update,
    context,
    mocked_reply_markup,
):
    """
    Проверяем, что help handler, возвращает нужное сообщение
    и нужную клавиатуру.
    """
    update.message = AsyncMock()
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)

    await command_handlers.help(update, context)

    update.message.reply_html.assert_called_with(
        text=await get_message_bot("help_message"),
        reply_markup=help_keyboard_markup,
    )
