from telegram import InlineKeyboardButton, InlineKeyboardMarkup

PARTICIPATE = "Участвовать!"
SUPPORT = "Написать в поддержку"

keyboard_buttons = [
    [
        InlineKeyboardButton(PARTICIPATE, callback_data="go_bot"),
        InlineKeyboardButton(SUPPORT, callback_data="support_bot"),
    ]
]
help_keyboard = InlineKeyboardMarkup(keyboard_buttons)
