from bot.models import Recruiter, Student


async def user_is_exist(user_id: int) -> bool:
    """Проверяет наличие юзера в базе данных."""
    if (
        await Recruiter.objects.filter(telegram_id=user_id).aexists()
        or await Student.objects.filter(telegram_id=user_id).aexists()
    ):
        return True
    return False


async def deleting_account(user_id: int) -> None:
    """Фунция удаления аккаунта."""
    if await Recruiter.objects.filter(telegram_id=user_id).aexists():
        await Recruiter.objects.filter(telegram_id=user_id).adelete()
    else:
        await Student.objects.filter(telegram_id=user_id).adelete()
