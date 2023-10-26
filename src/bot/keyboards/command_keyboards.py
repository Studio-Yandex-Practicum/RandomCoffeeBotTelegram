from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    GO_BUTTON,
    NEXT_TIME_BUTTON,
    PARTICIPATE_BUTTON,
    SUPPORT_BUTTON,
)
from bot.utils.url_form import get_form_url

start_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=GO_BUTTON, callback_data="go"),
            InlineKeyboardButton(
                text=NEXT_TIME_BUTTON, callback_data="next_time"
            ),
        ]
    ]
)


async def create_support_keyboard():
    """Создание кнопки со ссылкой на форму поддержки."""
    support_form_url = await get_form_url("support_form")
    support_keyboard_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=SUPPORT_BUTTON,
                    callback_data="Get support",
                    url=support_form_url,
                )
            ]
        ]
    )
    return support_keyboard_markup


help_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                PARTICIPATE_BUTTON, callback_data="participate"
            ),
            InlineKeyboardButton(SUPPORT_BUTTON, callback_data="support"),
        ]
    ]
)
