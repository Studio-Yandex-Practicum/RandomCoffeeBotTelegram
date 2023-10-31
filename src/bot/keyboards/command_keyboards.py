from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    GO_BUTTON,
    NEXT_TIME_BUTTON,
    PARTICIPATE_BUTTON,
    SUPPORT_BUTTON,
)
from bot.constants.links import FORM_KEYS
from bot.utils.form_url import get_form_url

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


async def create_support_keyboard() -> InlineKeyboardMarkup:
    """Создание кнопки со ссылкой на форму поддержки."""
    support_url = await get_form_url(FORM_KEYS["SUPPORT"])
    support_keyboard_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=SUPPORT_BUTTON,
                    callback_data="Get support",
                    url=support_url,
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
