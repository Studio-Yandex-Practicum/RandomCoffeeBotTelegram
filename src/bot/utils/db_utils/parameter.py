from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from loguru import logger

from bot.models import ParameterBot


async def get_parameter_bot(parameter_key: str) -> Optional[str]:
    """Возвращает параметр бота."""
    try:
        parameter_bot = await ParameterBot.objects.aget(
            parameter_key=parameter_key
        )
        return parameter_bot.value
    except ObjectDoesNotExist as error:
        logger.error(f"Error in getting objects in database: {error}")
