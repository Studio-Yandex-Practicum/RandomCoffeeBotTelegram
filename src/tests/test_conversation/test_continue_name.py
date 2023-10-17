from unittest.mock import AsyncMock

import pytest

from bot.constants.messages import CHOOSE_PROFESSION_MESSAGE
from bot.handlers.conversation_handlers import continue_name
from bot.keyboards.conversation_keyboards import profession


@pytest.mark.asyncio
async def test_continue_name_student_role(update, context, db):
    """
    Проверяем, что continue_name handler
    возвращает нужное сообщение и клавиатуру
    если выбрана роль студента.
    """
    update.callback_query = AsyncMock()
    context.user_data = {"role": "student"}
    await continue_name(update, context)
    update.callback_query.edit_message_text.assert_awaited_with(
        CHOOSE_PROFESSION_MESSAGE
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        reply_markup=await profession()
    )


@pytest.mark.asyncio
async def test_continue_name_recruiter_role(update, context):
    """
    Проверяем, что continue_name handler
    ставит роль It-рекрутер
    если роль не студент.
    """
    update.callback_query = AsyncMock()
    context.user_data = {"role": "", "name": "test_user"}

    await continue_name(update, context)

    assert context.user_data["profession"] == "It-рекрутер"
