from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import START_BUTTON

next_time_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=START_BUTTON, callback_data="start")]]
)
