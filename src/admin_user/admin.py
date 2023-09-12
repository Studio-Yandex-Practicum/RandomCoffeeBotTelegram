from django.contrib import admin
from django.contrib.auth import get_user_model

Admin = get_user_model()


@admin.register(Admin)
class AdminUser(admin.ModelAdmin):
    """Управление админкой."""
