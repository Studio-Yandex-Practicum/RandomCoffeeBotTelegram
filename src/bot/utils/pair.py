from http import HTTPStatus

from loguru import logger

from bot.models import CreatedPair, Recruiter, Student


async def make_pair(student: Student, recruiter: Recruiter) -> HTTPStatus:
    """Функция для создания пары студент-рекрутер."""
    try:
        student.has_pair = True
        recruiter.has_pair = True
        created_pair = await CreatedPair.objects.acreate(
            student=student, recruiter=recruiter
        )
        await student.asave()
        await recruiter.asave()
        status = HTTPStatus.OK
        logger.info(f"The pair was made with {created_pair}")
    except Exception as exp:
        status = HTTPStatus.BAD_REQUEST
        logger.error(
            (
                f"Error in making pair with {student.name} "
                f"and {recruiter.name}: {exp}"
            )
        )
    return status
