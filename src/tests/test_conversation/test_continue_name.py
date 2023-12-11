from unittest.mock import AsyncMock, Mock, patch

import pytest
from django.conf import settings
from telegram.constants import ParseMode

from bot.utils.db_utils.message import get_message_bot
from bot.handlers.conversation_handlers import continue_name


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_continue_name_itspecialist_role(
    update, context, pagination_keyboard, mocked_pagination_reply_markup
):
    """
    Проверяем, что continue_name handler
    возвращает нужное сообщение и клавиатуру
    если выбрана роль IT-специалиста.
    """
    update.callback_query = AsyncMock()
    context.user_data = {"role": "itspecialist"}

    with (
        patch(
            "bot.handlers.conversation_handlers.build_profession_keyboard",
            Mock(return_value=pagination_keyboard),
        ),
        patch(
            "bot.handlers.conversation_handlers.parse_callback_data",
            Mock(return_value=settings.DEFAULT_PAGE),
        ),
    ):
        await continue_name(update, context)

    update.callback_query.edit_message_text.assert_awaited_with(
        await get_message_bot("choose_profession_message"),
        parse_mode=ParseMode.HTML,
    )
    update.callback_query.edit_message_reply_markup.assert_awaited_with(
        reply_markup=mocked_pagination_reply_markup
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_continue_name_recruiter_role(update, context):
    """
    Проверяем, что continue_name handler
    ставит роль It-рекрутер
    если роль не IT-специалист.
    """
    update.callback_query = AsyncMock()
    context.user_data = {"role": "", "name": "test_user"}

    await continue_name(update, context)

    assert context.user_data["profession"] == "It-рекрутер"
