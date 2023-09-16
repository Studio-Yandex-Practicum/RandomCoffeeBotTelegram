from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_buttons = [
    [
        InlineKeyboardButton("Учавствовать!", callback_data="go_bot"),
        InlineKeyboardButton(
            "Написать в поддержку", callback_data="support_bot"
        ),
    ]
]
help_keyboard = InlineKeyboardMarkup(keyboard_buttons)
