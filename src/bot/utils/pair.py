from django.db import IntegrityError
from loguru import logger

from bot.models import CreatedPair, Recruiter, Student


async def make_pair(student: Student, recruiter: Recruiter) -> bool:
    """Функция для создания пары студент-рекрутер."""
    status = False
    try:
        student.has_pair = True
        recruiter.has_pair = True
        created_pair = await CreatedPair.objects.acreate(
            student=student, recruiter=recruiter
        )
        await student.asave(update_fields=["has_pair"])
        await recruiter.asave(update_fields=["has_pair"])
        logger.info(f"The pair was made with {created_pair}")
        status = True
    except IntegrityError as error:
        logger.error(f"Error in creating objects in database: {error}")
    except Exception as exp:
        logger.error(
            (
                f"Error in making pair with {student.name} "
                f"and {recruiter.name}: {exp}"
            )
        )
    return status
