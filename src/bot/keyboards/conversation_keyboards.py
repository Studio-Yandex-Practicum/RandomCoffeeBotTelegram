from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    CHANGE_NAME_BUTTON,
    CONTINUE_BUTTON,
)

guess_name_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=CONTINUE_BUTTON, callback_data="continue_name"
            )
        ],
        [
            InlineKeyboardButton(
                text=CHANGE_NAME_BUTTON, callback_data="change_name"
            )
        ],
    ]
)
