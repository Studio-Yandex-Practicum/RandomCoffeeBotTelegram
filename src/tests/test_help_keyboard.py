import pytest

from bot.constants.buttons import PARTICIPATE_BUTTON, SUPPORT_BUTTON
from bot.keyboards.command_keyboards import help_keyboard_markup
from bot.constants.messages import GO, SUPPORT


LENGHT_START_KEYBOARD = 2
INDEX_TEXT = 0
INDEX_CALLBACK = 1
messages = ([PARTICIPATE_BUTTON, GO], [SUPPORT_BUTTON, SUPPORT])


@pytest.mark.asyncio
async def test_help_keyboard():
    """Проверяем, что help_keyboard, возвращает сообщение и кнопку."""

    for number_of_message, inline_keyboard_button in enumerate(
        *help_keyboard_markup.inline_keyboard
    ):
        assert (
            inline_keyboard_button.text
            == messages[number_of_message][INDEX_TEXT]
        )
        assert (
            inline_keyboard_button.callback_data
            == messages[number_of_message][INDEX_CALLBACK]
        )
    assert len(*help_keyboard_markup.inline_keyboard) == LENGHT_START_KEYBOARD
