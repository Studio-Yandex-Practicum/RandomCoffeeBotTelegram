from admin_user.actions import (
    delete_inactive_users,
    delete_users_and_send_message,
)
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from bot.models import (
    CreatedPair,
    FormUrl,
    ItSpecialist,
    MessageBot,
    ParameterBot,
    PassedPair,
    Profession,
    Recruiter,
)
from bot.utils.forms import ItSpecialistForm, RecruiterForm

csrf_protect_m = method_decorator(csrf_protect)


class BaseItSpecialistRecruiterAdmin(admin.ModelAdmin):
    """Базовый класс админки IT-специалистов и рекрутеров."""

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        Вызывает функцию 'delete_inactive_users'
        в обход валидации методов базового класса.
        """
        if (
            "action" in request.POST
            and request.POST["action"] == "delete_inactive_users"
        ):
            delete_inactive_users(self.model)
            return HttpResponseRedirect(request.path)
        return super().changelist_view(request, extra_context)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """Управление профессиями."""

    list_display = ("name",)
    exclude = ("professional_key",)
    icon_name = "card_travel"


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
    icon_name = "people"


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
    icon_name = "people_outline"


@admin.register(ItSpecialist)
class ItSpecialistAdmin(BaseItSpecialistRecruiterAdmin):
    """Управление моделью IT-специалиста."""

    form = ItSpecialistForm
    fields = (
        "name",
        "surname",
        "profession",
        "has_pair",
        "in_search_pair",
        "telegram_id",
        "telegram_username",
        "last_login_date",
        "registration_date",
    )
    readonly_fields = (
        "has_pair",
        "in_search_pair",
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
        "in_search_pair",
        "last_login_date",
        "registration_date",
    )
    list_filter = (
        "registration_date",
        "last_login_date",
        "profession",
        "has_pair",
        "in_search_pair",
    )
    search_fields = ("telegram_id", "telegram_username")
    actions = (delete_users_and_send_message, delete_inactive_users)
    icon_name = "school"


@admin.register(Recruiter)
class RecruiterAdmin(BaseItSpecialistRecruiterAdmin):
    """Управление моделью рекрутера."""

    fields = (
        "name",
        "surname",
        "has_pair",
        "in_search_pair",
        "telegram_id",
        "telegram_username",
        "registration_date",
        "last_login_date",
    )
    readonly_fields = (
        "has_pair",
        "in_search_pair",
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
        "in_search_pair",
        "last_login_date",
        "registration_date",
    )
    list_filter = (
        "registration_date",
        "last_login_date",
        "has_pair",
        "in_search_pair",
        "last_login_date",
        "registration_date",
    )
    search_fields = ("telegram_id", "telegram_username")
    actions = (delete_users_and_send_message, delete_inactive_users)
    icon_name = "person"


@admin.register(FormUrl)
class FormUrlAdmin(admin.ModelAdmin):
    """Управление моделью ссылок на формы."""

    list_display = (
        "title",
        "url",
    )
    list_filter = ("title",)
    search_fields = ("title",)
    icon_name = "link"

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
    icon_name = "message"

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять сообщения."""
        return False

    def has_add_permission(self, request):
        """Запрещает создавать новые сообщения."""
        return False


@admin.register(ParameterBot)
class ParameterBotAdmin(admin.ModelAdmin):
    """Управление моделью параметров бота."""

    list_display = (
        "title",
        "value",
        "unit_measurement",
    )
    list_filter = ("title",)
    search_fields = ("title",)
    exclude = ("parameter_key",)
    icon_name = "settings"

    def has_delete_permission(self, request, obj=None):
        """Запрещает удалять параметры."""
        return False

    def has_add_permission(self, request):
        """Запрещает создавать новые параметры."""
        return False
