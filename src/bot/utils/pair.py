from django.db import IntegrityError
from loguru import logger

from bot.constants.states import States
from bot.models import CreatedPair, Recruiter, Student


async def make_pair(student: Student, recruiter: Recruiter) -> States:
    """Функция для создания пары студент-рекрутер."""
    try:
        student.has_pair = True
        recruiter.has_pair = True
        created_pair = await CreatedPair.objects.acreate(
            student=student, recruiter=recruiter
        )
        await student.asave()
        await recruiter.asave()
        state = States.PAIR_FOUND
        logger.info(f"The pair was made with {created_pair}")
    except IntegrityError as error:
        state = States.PAIR_NOT_FOUND
        logger.error(f"Error in creating objects in database: {error}")
    except Exception as exp:
        state = States.PAIR_NOT_FOUND
        logger.error(
            (
                f"Error in making pair with {student.name} "
                f"and {recruiter.name}: {exp}"
            )
        )
    return state
