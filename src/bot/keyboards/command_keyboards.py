from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import GO_BUTTON, NEXT_TIME_BUTTON, SUPPORT_BUTTON

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


def support_keyboard() -> InlineKeyboardButton:
    """Build telegram assistance keyboard."""
    return InlineKeyboardButton(
        text=SUPPORT_BUTTON,
        callback_data="Get support",
    )
