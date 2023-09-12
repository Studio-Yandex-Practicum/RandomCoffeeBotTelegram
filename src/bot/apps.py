from django_asgi_lifespan.signals import asgi_shutdown

from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def stop_bot(self, **kwargs):
        self.bot.stop()

    def ready(self) -> None:
        from .bot import Bot
        self.bot = Bot()

        asgi_shutdown.connect(self.stop_bot)

        self.bot.start()
