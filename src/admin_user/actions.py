import asyncio
import datetime as dt

from django.apps import apps
from django.contrib import admin

from bot.constants.cases import PARENT_CASE_ROLE
from bot.models import ParameterBot
from bot.utils.message_senders import send_deleting_from_db_message


@admin.action(description="Удалить пользователей и оповестить их в телеграмме")
def delete_users_and_send_message(modeladmin, request, queryset):
    """Действие для удаления пользователей и оповещение их в телеграмме."""
    users = queryset.values("telegram_id", "telegram_username")
    app_config = apps.get_app_config("bot")
    bot = app_config.bot
    job_queue = asyncio.run(bot.get_job_queue())
    for user in users:
        job_queue.run_once(
            callback=send_deleting_from_db_message,
            when=0,
            user_id=user["telegram_id"],
            name=user["telegram_username"],
            data=PARENT_CASE_ROLE[queryset.model],
        )
    queryset.delete()


@admin.action(description="Удалить неактивных пользователей")
def delete_inactive_users(modeladmin):
    """Удаляет неактивных пользователей."""
    days = ParameterBot.objects.get(parameter_key="inactive_users_day").value
    date = dt.datetime.now() - dt.timedelta(days=days)
    modeladmin.objects.filter(last_login_date__lte=date).delete()
