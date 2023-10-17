from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ALL_RIGHT_BUTTON,
    CHANGE_NAME_BUTTON,
    CONTINUE_BUTTON,
    FILL_AGAIN_BUTTON,
    NO_BUTTON,
    RECRUITER_ROLE_BUTTON,
    START_BUTTON,
    STUDENT_ROLE_BUTTON,
    YES_BUTTON,
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
            ),
            InlineKeyboardButton(
                text=CHANGE_NAME_BUTTON, callback_data="change_name"
            ),
        ],
    ]
)

profile_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=ALL_RIGHT_BUTTON, callback_data="all_right"
            ),
            InlineKeyboardButton(
                text=FILL_AGAIN_BUTTON, callback_data="fill_again"
            ),
        ],
    ]
)

is_pair_successful_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=YES_BUTTON, callback_data="yes"),
            InlineKeyboardButton(text=NO_BUTTON, callback_data="no"),
        ],
    ]
)


def profession(data) -> InlineKeyboardMarkup:
    """Получение inline кнопок для профессий."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=profession.name,
                    callback_data=profession.professional_key,
                )
            ]
            for profession in data
        ]
    )
