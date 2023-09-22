import pytest

from bot.constants.buttons import GO_BUTTON, NEXT_TIME_BUTTON
from bot.constants.constant import (
    LENGHT_START_KEYBOARD,
    BUTTON_TEXT,
    BUTTON_CALLBACK,
)
from bot.constants.messages import NEXT_TIME, GO
from bot.keyboards.command_keyboards import start_keyboard_markup


messages = ([GO_BUTTON, GO], [NEXT_TIME_BUTTON, NEXT_TIME])


@pytest.mark.asyncio
async def test_start_keyboard():
    """Проверяем, что start_keyboard, возвращает сообщение и кнопку."""

    for number_of_message, inline_keyboard_button in enumerate(
        *start_keyboard_markup.inline_keyboard
    ):
        assert (
            inline_keyboard_button.text
            == messages[number_of_message][BUTTON_TEXT]
        )
        assert (
            inline_keyboard_button.callback_data
            == messages[number_of_message][BUTTON_CALLBACK]
        )
    assert len(*start_keyboard_markup.inline_keyboard) == LENGHT_START_KEYBOARD
