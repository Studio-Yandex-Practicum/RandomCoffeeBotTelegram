from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from loguru import logger

from bot.models import MessageBot


async def get_message_bot(message_key: str) -> Union[None, str]:
    """Возвращает сообщение бота."""
    try:
        message_bot = await MessageBot.objects.aget(message_key=message_key)
        return message_bot.message
    except ObjectDoesNotExist as error:
        logger.error(f"Error in getting objects in database: {error}")
