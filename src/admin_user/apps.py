from django.apps import AppConfig


class AdminUserConfig(AppConfig):
    """Настройка приложения admin_user."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_user"

    def ready(self):
        """Установка сигналов."""
        import admin_user.signals  # noqa
