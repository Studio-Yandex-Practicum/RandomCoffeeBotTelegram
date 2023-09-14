from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown


class BotConfig(AppConfig):
    """Конфигурация приложения бота."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def stop_bot(self, **kwargs):
        """Вызывается при остановке приложения."""
        self.bot.stop()

    def ready(self) -> None:
        """Вызывается при запуске приложения."""
        from bot.bot_interface import Bot

        self.bot = Bot()

        asgi_shutdown.connect(self.stop_bot)

        self.bot.start()
