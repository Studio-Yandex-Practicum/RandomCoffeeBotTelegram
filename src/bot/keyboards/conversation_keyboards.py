from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    CHANGE_NAME_BUTTON,
    CONTINUE_BUTTON,
    RECRUITER_ROLE_BUTTON,
    START_BUTTON,
    STUDENT_ROLE_BUTTON,
)

restart_keyboard_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=START_BUTTON, callback_data="restart")]]
)

role_choice_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=STUDENT_ROLE_BUTTON, callback_data="student"
            )
        ],
        [
            InlineKeyboardButton(
                text=RECRUITER_ROLE_BUTTON, callback_data="recruiter"
            )
        ],
    ]
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
