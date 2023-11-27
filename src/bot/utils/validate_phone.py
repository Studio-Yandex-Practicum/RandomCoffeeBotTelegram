import re

from bot.constants.patterns import PHONE_NUMBER_PATTERN


async def validation_phone_number(phone: str) -> bool:
    """Проверка номера телефона."""
    return True if re.fullmatch(PHONE_NUMBER_PATTERN, phone) else False
