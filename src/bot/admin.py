from django.contrib import admin

from .models import CreatedPair, PassedPair, Recruiter, Student


@admin.register(CreatedPair)
class CreatedPairAdmin(admin.ModelAdmin):
    """Управление созданной парой."""

    list_display = ("id", "student", "recruiter", "date")
    list_filter = ("date",)
    search_fields = (
        "student__user_id",
        "recruiter__user_id",
        "student__tg_username",
        "recruiter__tg_username",
    )


@admin.register(PassedPair)
class PassedPairAdmin(admin.ModelAdmin):
    """Управление моделью созвона."""

    list_display = (
        "id",
        "student",
        "recruiter",
        "date",
        "is_interview_successful",
    )
    list_filter = ("date", "is_interview_successful")
    search_fields = (
        "student__user_id",
        "recruiter__user_id",
        "student__tg_username",
        "recruiter__tg_username",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление моделью студента."""

    list_display = (
        "user_id",
        "name",
        "surname",
        "tg_username",
        "registration_date",
        "last_login_date",
        "is_vacant",
    )
    list_filter = ("registration_date", "last_login_date", "is_vacant")
    search_fields = ("user_id", "tg_username")


@admin.register(Recruiter)
class RecruterAdmin(admin.ModelAdmin):
    """Управление моделью рекрутера."""

    list_display = (
        "user_id",
        "name",
        "surname",
        "tg_username",
        "registration_date",
        "last_login_date",
        "is_vacant",
    )
    list_filter = ("registration_date", "last_login_date", "is_vacant")
    search_fields = ("user_id", "tg_username")
