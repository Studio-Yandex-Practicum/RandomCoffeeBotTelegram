from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    GO_BUTTON,
    NEXT_TIME_BUTTON,
    PARTICIPATE,
    SUPPORT,
)

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

help_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(PARTICIPATE, callback_data="go"),
            InlineKeyboardButton(SUPPORT, callback_data="support"),
        ]
    ]
)
