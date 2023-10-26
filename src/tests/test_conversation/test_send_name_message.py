from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import GUESS_NAME_MESSAGE
from bot.handlers.conversation_handlers import send_name_message
from bot.keyboards.conversation_keyboards import guess_name_keyboard_markup


@pytest.mark.asyncio
async def test_send_name_message_with_callback_query(update, context):
    """
    Тест проверяет, что функция send_name_message корректно отправляет
    сообщение и обновляет клавиатуру при наличии callback_query.
    """
    update.callback_query = AsyncMock()
    context.user_data = {"name": "test"}

    await send_name_message(update, context)

    update.callback_query.answer.assert_awaited_once()
    update.callback_query.edit_message_text.assert_awaited_with(
        GUESS_NAME_MESSAGE.format(context.user_data.get("name"))
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        guess_name_keyboard_markup
    )


@pytest.mark.asyncio
async def test_send_name_message_without_callback_query(update, context):
    """
    Тест проверяет, что функция send_name_message корректно отправляет
    сообщение и устанавливает клавиатуру, если callback_query отсутствует.
    """
    update.callback_query = None
    update.message = AsyncMock()
    context.user_data = {"name": "test"}

    await send_name_message(update, context)

    update.message.reply_text.assert_awaited_with(
        GUESS_NAME_MESSAGE.format(context.user_data.get("name")),
        reply_markup=guess_name_keyboard_markup,
    )
