from django.db import IntegrityError
from loguru import logger

from bot.models import CreatedPair, PassedPair, Recruiter, Student


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


async def delete_pair(
    student: Student, recruiter: Recruiter, interview_successful: bool
) -> bool:
    """Функция для удаления пары студент-рекрутер."""
    try:
        student.has_pair = False
        recruiter.has_pair = False
        await CreatedPair.objects.filter(
            student=student, recruiter=recruiter
        ).adelete()
        passed_pair = await PassedPair.objects.acreate(
            student=student,
            recruiter=recruiter,
            interview_successful=interview_successful,
        )
        await student.asave(update_fields=["has_pair"])
        await recruiter.asave(update_fields=["has_pair"])
        logger.debug(f"The passed  pair was made with {passed_pair}")
        return True
    except IntegrityError as error:
        logger.error(f"Error in creating objects in database: {error}")
    except Exception as error:
        logger.error(
            (
                f"Error in delete pair with {student.name} "
                f"and {recruiter.name}: {error}"
            )
        )
    return False
