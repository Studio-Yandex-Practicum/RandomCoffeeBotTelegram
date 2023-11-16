from django.db import IntegrityError
from loguru import logger

from bot.models import CreatedPair, PassedPair, Recruiter, ItSpecialist


async def make_pair(itspecialist: ItSpecialist, recruiter: Recruiter) -> bool:
    """Функция для создания пары IT-специалист - рекрутер."""
    status = False
    try:
        itspecialist.has_pair = True
        recruiter.has_pair = True
        created_pair = await CreatedPair.objects.acreate(
            itspecialist=itspecialist, recruiter=recruiter
        )
        await itspecialist.asave(update_fields=["has_pair"])
        await recruiter.asave(update_fields=["has_pair"])
        logger.info(f"The pair was made with {created_pair}")
        status = True
    except IntegrityError as error:
        logger.error(f"Error in creating objects in database: {error}")
    except Exception as exp:
        logger.error(
            (
                f"Error in making pair with {itspecialist.name} "
                f"and {recruiter.name}: {exp}"
            )
        )
    return status


async def delete_pair(
    itspecialist: ItSpecialist,
    recruiter: Recruiter,
    interview_successful: bool
) -> bool:
    """Функция для удаления пары IT-специалист - рекрутер."""
    try:
        itspecialist.has_pair = False
        recruiter.has_pair = False
        await CreatedPair.objects.filter(
            itspecialist=itspecialist, recruiter=recruiter
        ).adelete()
        passed_pair = await PassedPair.objects.acreate(
            itspecialist=itspecialist,
            recruiter=recruiter,
            interview_successful=interview_successful,
        )
        await itspecialist.asave(update_fields=["has_pair"])
        await recruiter.asave(update_fields=["has_pair"])
        logger.debug(f"The passed  pair was made with {passed_pair}")
        return True
    except IntegrityError as error:
        logger.error(f"Error in creating objects in database: {error}")
    except Exception as error:
        logger.error(
            (
                f"Error in delete pair with {itspecialist.name} "
                f"and {recruiter.name}: {error}"
            )
        )
    return False
