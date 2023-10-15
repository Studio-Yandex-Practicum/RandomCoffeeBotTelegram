from django.contrib import admin

from bot.models import (
    CreatedPair,
    FormUrl,
    PassedPair,
    Profession,
    Recruiter,
    Student,
)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """Управление профессиями."""

    list_display = ("name",)


@admin.register(CreatedPair)
class CreatedPairAdmin(admin.ModelAdmin):
    """Управление созданной парой."""

    list_display = ("id", "student", "recruiter", "date")
    list_filter = ("date",)
    search_fields = (
        "student__telegram_id",
        "recruiter__telegram_id",
        "student__telegram_username",
        "recruiter__telegram_username",
    )


@admin.register(PassedPair)
class PassedPairAdmin(admin.ModelAdmin):
    """Управление моделью созвона."""

    list_display = (
        "id",
        "student",
        "recruiter",
        "date",
        "interview_successful",
    )
    list_filter = ("date", "interview_successful")
    search_fields = (
        "student__telegram_id",
        "recruiter__telegram_id",
        "student__telegram_username",
        "recruiter__telegram_username",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление моделью студента."""

    list_display = (
        "telegram_id",
        "name",
        "surname",
        "telegram_username",
        "registration_date",
        "last_login_date",
        "has_pair",
    )
    list_filter = ("registration_date", "last_login_date", "has_pair")
    search_fields = ("telegram_id", "telegram_username")


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    """Управление моделью рекрутера."""

    list_display = (
        "telegram_id",
        "name",
        "surname",
        "telegram_username",
        "registration_date",
        "last_login_date",
        "has_pair",
    )
    list_filter = ("registration_date", "last_login_date", "has_pair")
    search_fields = ("telegram_id", "telegram_username")


@admin.register(FormUrl)
class FormUrlAdmin(admin.ModelAdmin):
    """Управление моделью ссылок на формы."""

    list_display = (
        "title",
        "url",
        "url_key",
    )
    list_filter = ("title", "url_key")
    search_fields = ("title", "url_key")

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять ссылки."""
        return False

    def has_add_permission(self, request):
        """Запрещает создавать новые ссылки."""
        return False
