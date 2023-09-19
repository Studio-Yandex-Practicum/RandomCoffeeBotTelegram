from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import GO_BUTTON, NEXT_TIME_BUTTON, SUPPORT_BUTTON
from bot.constants.links import SUPPORT_FORM

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

support_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=SUPPORT_BUTTON,
                callback_data="Get support",
                url=SUPPORT_FORM,
            )
        ]
    ]
)
