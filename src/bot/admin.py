from admin_user.actions import delete_users_and_send_message
from django.contrib import admin

from bot.models import (
    CreatedPair,
    FormUrl,
    ItSpecialist,
    MessageBot,
    PassedPair,
    Profession,
    Recruiter,
)
from bot.utils.forms import ItSpecialistForm, RecruiterForm


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """Управление профессиями."""

    list_display = ("name",)
    exclude = ("professional_key",)


@admin.register(CreatedPair)
class CreatedPairAdmin(admin.ModelAdmin):
    """Управление созданной парой."""

    list_display = ("id", "itspecialist", "recruiter", "date")
    list_filter = ("date",)
    search_fields = (
        "itspecialist__telegram_id",
        "recruiter__telegram_id",
        "itspecialist__telegram_username",
        "recruiter__telegram_username",
    )


@admin.register(PassedPair)
class PassedPairAdmin(admin.ModelAdmin):
    """Управление моделью созвона."""

    list_display = (
        "id",
        "itspecialist",
        "recruiter",
        "date",
        "interview_successful",
    )
    list_filter = ("date", "interview_successful")
    search_fields = (
        "itspecialist__telegram_id",
        "recruiter__telegram_id",
        "itspecialist__telegram_username",
        "recruiter__telegram_username",
    )


@admin.register(ItSpecialist)
class ItSpecialistAdmin(admin.ModelAdmin):
    """Управление моделью IT-специалиста."""

    form = ItSpecialistForm
    fields = (
        "name",
        "surname",
        "profession",
        "has_pair",
        "telegram_id",
        "telegram_username",
        "last_login_date",
        "registration_date",
    )
    readonly_fields = (
        "telegram_id",
        "telegram_username",
        "last_login_date",
        "registration_date",
    )
    list_display = (
        "name",
        "surname",
        "telegram_id",
        "telegram_username",
        "profession",
        "has_pair",
        "last_login_date",
        "registration_date",
    )
    list_filter = (
        "registration_date",
        "last_login_date",
        "profession",
        "has_pair",
    )
    list_filter = (
        "registration_date",
        "last_login_date",
        "profession",
        "has_pair",
    )
    search_fields = ("telegram_id", "telegram_username")
    actions = [delete_users_and_send_message]


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    """Управление моделью рекрутера."""

    fields = (
        "name",
        "surname",
        "has_pair",
        "telegram_id",
        "telegram_username",
        "registration_date",
        "last_login_date",
    )
    readonly_fields = (
        "telegram_id",
        "telegram_username",
        "last_login_date",
        "registration_date",
    )
    form = RecruiterForm
    list_display = (
        "name",
        "surname",
        "telegram_id",
        "telegram_username",
        "has_pair",
        "last_login_date",
        "registration_date",
    )
    list_filter = ("registration_date", "last_login_date", "has_pair")
    search_fields = ("telegram_id", "telegram_username")
    actions = [delete_users_and_send_message]


@admin.register(FormUrl)
class FormUrlAdmin(admin.ModelAdmin):
    """Управление моделью ссылок на формы."""

    list_display = (
        "title",
        "url",
    )
    list_filter = ("title",)
    search_fields = ("title",)

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять ссылки."""
        return False

    def has_add_permission(self, request):
        """Запрещает создавать новые ссылки."""
        return False


@admin.register(MessageBot)
class MessageBotAdmin(admin.ModelAdmin):
    """Управление моделью сообщений бота."""

    list_display = (
        "title",
        "message",
    )
    list_filter = ("title",)
    search_fields = ("title",)
    exclude = ("message_key",)

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять сообщения."""
        return False

    def has_add_permission(self, request):
        """Запрещает создавать новые сообщения."""
        return False
