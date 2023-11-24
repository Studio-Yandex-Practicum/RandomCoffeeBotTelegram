from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from bot.models import ItSpecialist, Profession, Recruiter


async def to_create_user_in_db(
    update: Update, context: CallbackContext
) -> None:
    """Сохраняет пользователя в базе данных."""
    query = update.callback_query
    user_data = {
        "telegram_id": query.from_user.id,
        "name": context.user_data["name"],
        "surname": query.from_user.last_name,
        "telegram_username": context.user_data["contact"],
    }
    try:
        if context.user_data["role"] == "recruiter":
            await Recruiter.objects.acreate(**user_data)
        else:
            profession = await Profession.objects.aget(
                name=context.user_data["profession"]
            )
            await ItSpecialist.objects.acreate(
                profession=profession, **user_data
            )
    except Exception as error:
        logger.error(f"Не удалось сохранить данные в таблицу: {error}")


async def user_is_exist(user_id: int) -> bool:
    """Проверяет наличие юзера в базе данных."""
    if (
        await Recruiter.objects.filter(telegram_id=user_id).aexists()
        or await ItSpecialist.objects.filter(telegram_id=user_id).aexists()
    ):
        return True
    return False


async def deleting_account(user_id: int) -> None:
    """Фунция удаления аккаунта."""
    if await Recruiter.objects.filter(telegram_id=user_id).aexists():
        await Recruiter.objects.filter(telegram_id=user_id).adelete()
    else:
        await ItSpecialist.objects.filter(telegram_id=user_id).adelete()


async def update_last_login_date(user_id: int) -> None:
    """Функция обновления последнего входа юзера."""
    if await Recruiter.objects.filter(telegram_id=user_id).aexists():
        user = await Recruiter.objects.filter(telegram_id=user_id).afirst()
    else:
        user = await ItSpecialist.objects.filter(telegram_id=user_id).afirst()
    await user.asave()
