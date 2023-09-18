from telegram import InlineKeyboardButton

from bot.constants.buttons import SUPPORT_BUTTON


def support_keyboard() -> InlineKeyboardButton:
    """Build telegram assistance keyboard."""
    return InlineKeyboardButton(
        text=SUPPORT_BUTTON,
        callback_data="Get support",
    )
