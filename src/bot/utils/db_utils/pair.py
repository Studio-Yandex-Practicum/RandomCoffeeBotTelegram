from typing import Union

from django.db import IntegrityError
from django.utils import timezone
from loguru import logger

from bot.models import CreatedPair, ItSpecialist, PassedPair, Recruiter


async def make_pair(itspecialist: ItSpecialist, recruiter: Recruiter) -> bool:
    """Функция для создания пары IT-специалист-рекрутер."""
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
    interview_successful: bool,
) -> bool:
    """Функция для удаления пары IT-специалист-рекрутер."""
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


async def get_active_pair(role: str, user_id: int) -> Union[CreatedPair, None]:
    """Возвращает активную пару, с участием пользователя."""
    if role == "itspecialist":
        return (
            await CreatedPair.objects.filter(itspecialist=user_id)
            .select_related("itspecialist", "recruiter")
            .afirst()
        )
    else:
        return (
            await CreatedPair.objects.filter(recruiter=user_id)
            .select_related("itspecialist", "recruiter")
            .afirst()
        )


async def get_current_user(
    model: Union[ItSpecialist, Recruiter], telegram_id: int
) -> Union[ItSpecialist, Recruiter]:
    """Возвращает пользователя по telegram_id."""
    return await model.objects.aget(telegram_id=telegram_id)


async def set_now_search_start_time(
    user: Union[ItSpecialist, Recruiter]
) -> None:
    """Устанавливает время поиска по текущему."""
    user.search_start_time = timezone.now()
    await user.asave(update_fields=("search_start_time",))


async def get_user_for_pair(
    model: Union[ItSpecialist, Recruiter], role: str, telegram_id: int
) -> Union[ItSpecialist, Recruiter]:
    """Возвращает свободного пользователя для создания пары."""
    return (
        await model.objects.filter(has_pair=False)
        .exclude(**{f"passedpair__{role}": telegram_id})
        .order_by("search_start_time")
        .afirst()
    )
