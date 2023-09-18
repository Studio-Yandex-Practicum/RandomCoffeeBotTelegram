from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import GO_BUTTON, NEXT_TIME_BUTTON

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

help_command_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="HELP_ME", callback_data="go"),
        ]
    ]
)
