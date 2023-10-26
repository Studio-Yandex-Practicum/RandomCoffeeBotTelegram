import pytest

from bot.keyboards.conversation_keyboards import guess_name_keyboard_markup

LENGTH_START_KEYBOARD = 2
INDEX_TEXT = 0
INDEX_CALLBACK = 1
messages = (["Продолжить", "continue_name"], ["Сменить имя", "change_name"])


@pytest.mark.asyncio
async def test_guess_name_keyboard():
    """
    Тест проверяет, что клавиатура guess_name_keyboard_markup корректно
    формируется, с учетом текста и данных для callback на кнопках,
    а также общей длины клавиатуры.
    """
    for number_of_message, inline_keyboard_button in enumerate(
        *guess_name_keyboard_markup.inline_keyboard
    ):
        assert (
            inline_keyboard_button.text
            == messages[number_of_message][INDEX_TEXT]
        )
        assert (
            inline_keyboard_button.callback_data
            == messages[number_of_message][INDEX_CALLBACK]
        )
    assert (
        len(*guess_name_keyboard_markup.inline_keyboard)
        == LENGTH_START_KEYBOARD
    )
