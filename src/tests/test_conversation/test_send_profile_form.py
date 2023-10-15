from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import PROFILE_MESSAGE
from bot.handlers.conversation_handlers import send_profile_form
from bot.keyboards.conversation_keyboards import profile_keyboard_markup


@pytest.mark.asyncio
async def test_send_profile_form_with_callback_query(update, context):
    """
    Тест проверяет, что функция send_profile_form корректно отправляет
    сообщение и устанавливает клавиатуру, если callback_query отсутствует.
    """
    update.callback_query = AsyncMock()
    update.callback_query.from_user.username = "test_username"
    context.user_data = {
        "name": "test_name",
        "profession": "test_prof",
    }

    await send_profile_form(update, context)

    update.callback_query.edit_message_text.assert_awaited_with(
        PROFILE_MESSAGE.format(
            context.user_data["name"],
            context.user_data["profession"],
            context.user_data["contact"],
        )
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        profile_keyboard_markup
    )


@pytest.mark.asyncio
async def test_send_profile_form_without_callback_query(update, context):
    """
    Тест проверяет, что функция send_profile_form корректно отправляет
    сообщение и устанавливает клавиатуру, если callback_query отсутствует.
    """
    update.callback_query = None
    update.message = AsyncMock()
    context.user_data = {
        "name": "test_name",
        "profession": "test_prof",
        "contact": "test_username",
    }

    await send_profile_form(update, context)

    update.message.reply_text.assert_awaited_with(
        PROFILE_MESSAGE.format(
            context.user_data["name"],
            context.user_data["profession"],
            context.user_data["contact"],
        ),
        reply_markup=profile_keyboard_markup,
    )
