import pytest

from bot.keyboards.command_keyboards import support_keyboard_markup

FIRTS_KEYBOARD = 0


@pytest.mark.asyncio
async def test_support_keyboard():
    """
    Проверяем, что support_keyboard
    возвращает сообщение, ссылку и кнопку.
    """
    for inline_keyboard in support_keyboard_markup.inline_keyboard:
        assert inline_keyboard[FIRTS_KEYBOARD].text == "Написать в поддержку"
        assert inline_keyboard[FIRTS_KEYBOARD].callback_data == "Get support"
        assert inline_keyboard[FIRTS_KEYBOARD].url == "https://ya.ru"
        assert len(inline_keyboard) == 1
