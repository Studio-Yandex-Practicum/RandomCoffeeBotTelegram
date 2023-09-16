from telegram import InlineKeyboardButton

from bot.constants.buttons import SUPPORT_BUTTON


async def support_keyboard() -> InlineKeyboardButton:
    """Build telegram assistance keyboard async."""
    return InlineKeyboardButton(
        text=SUPPORT_BUTTON,
        callback_data="Get support",
    )
