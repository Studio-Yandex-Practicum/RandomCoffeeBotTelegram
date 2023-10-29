from admin_user.forms import UserChangeForm, UserCreationForm
from admin_user.utils.reset_password import send_password_reset_email
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

ADMIN_HEADER = "Администрирование RandomCoffeeBot"
ADMIN_TITLE = "Панель администратора бота"

AdminUser = get_user_model()

admin.site.unregister(Group)
admin.site.site_header = ADMIN_HEADER
admin.site.index_title = ADMIN_TITLE


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    """Управление админкой."""

    form = UserChangeForm
    add_form = UserCreationForm
    actions = ["reset_password"]

    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            _("Personal info"),
            {"fields": ("username", "first_name", "last_name")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    @admin.action(description="Сбросить пароль")
    def reset_password(self, request, queryset):
        """Send emails with password reset link to users."""
        for user in queryset:
            send_password_reset_email(user)
