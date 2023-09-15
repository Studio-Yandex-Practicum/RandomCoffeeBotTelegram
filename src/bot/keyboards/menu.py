from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import SUPPORT_BUTTON


async def support_keyboard() -> InlineKeyboardMarkup:
    """
    Build telegram assistance keyboard async.

    After building cache it.
    """
    return InlineKeyboardButton(
        text=SUPPORT_BUTTON,
        callback_data="Get support",
    )
