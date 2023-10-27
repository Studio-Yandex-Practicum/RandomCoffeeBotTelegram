import pytest
from unittest.mock import AsyncMock, patch

from bot.constants.buttons import SUPPORT_BUTTON
from bot.keyboards.command_keyboards import create_support_keyboard


@pytest.mark.asyncio
async def test_support_keyboard(db):
    """
    Проверяем, что support_keyboard
    возвращает сообщение, ссылку и кнопку.
    """
    support_keyboard_markup = await create_support_keyboard()
    button = support_keyboard_markup.inline_keyboard[0][0]
    assert button.text == SUPPORT_BUTTON
    assert button.callback_data == "Get support"
    assert button.url == "https://practicum.yandex.ru/"
