import asyncio

from django.apps import AppConfig


class BotConfig(AppConfig):
    """Config for bot app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def ready(self) -> None:
        """Start the bot application."""
        from .bot import start_bot

        asyncio.ensure_future(start_bot(), loop=asyncio.get_event_loop())
