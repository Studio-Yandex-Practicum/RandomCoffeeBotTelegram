from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


AdminUser = get_user_model()

admin.site.unregister(Group)
admin.site.site_header = "Администрирование RandomCoffeeBot"
admin.site.index_title = "Панель администратора бота"


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    """Управление админкой."""

    pass
