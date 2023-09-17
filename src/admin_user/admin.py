from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

AdminUser = get_user_model()


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    """Управление админкой."""

    pass
