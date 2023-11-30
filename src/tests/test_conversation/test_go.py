from unittest.mock import AsyncMock

import pytest

from bot.utils.db_utils.message import get_message_bot
from bot.constants.states import States
from bot.handlers.conversation_handlers import go
from bot.keyboards.conversation_keyboards import role_choice_keyboard_markup


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_go_user_is_no_exist(update, context):
    """
    Проверяем, что go handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователя не существует.
    """
    update.callback_query = AsyncMock()
    update.callback_query.from_user.id = 123
    result = await go(update, context)

    assert States.ROLE_CHOICE == result
    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("choose_role_message")
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        role_choice_keyboard_markup
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_go_user_is_exist(update, context, itspecialist):
    """
    Проверяем, что go handler возвращает
    нужное состояние, сообщение и клавиатуру
    если пользователь существует и пара отсутствует.
    """
    update.callback_query = AsyncMock()
    itspecialist = await itspecialist
    context.user_data = {"role": "itspecialist"}
    update.callback_query.from_user.id = itspecialist.telegram_id
    result = await go(update, context)
    update.callback_query.message.reply_text.assert_awaited_with(
        await get_message_bot("pair_search_message")
    )
    assert States.CALLING_IS_SUCCESSFUL == result
