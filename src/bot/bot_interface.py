import asyncio
import logging
from typing import Self

from django.conf import settings
from telegram.ext import Application, ApplicationBuilder, PicklePersistence

from .handlers import HANDLERS

logger = logging.getLogger(__name__)


class Bot:
    """Класс-синглтон для управления телеграм-ботом."""

    _instance: Self | None = None

    def __new__(cls, *args, **kwargs):
        """Синглтон-конструктор."""
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Инициализация бота."""
        self._app: Application | None = None
        self._stop_event = asyncio.Event()
        logger.info("Bot instance created.")

    def start(self) -> None:
        """Запускает бота."""
        logger.info("Bot starting...")
        self._stop_event.clear()
        asyncio.ensure_future(self._run(), loop=asyncio.get_event_loop())

    def stop(self) -> None:
        """Останавливает бота."""
        logger.info("Bot stopping...")
        self._stop_event.set()

    async def _run(self) -> None:
        """Главный асинхронный метод, управляющий жизненным циклом бота."""
        self._app = await self._build_app()
        await self._app.initialize()
        await self._manage_webhook()
        await self._start_bot()
        await self._stop_event.wait()
        await self._stop_bot()

    async def _build_app(self) -> Application:
        """Создает и настраивает ASGI-приложение для бота."""
        app = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_TOKEN)
            .persistence(PicklePersistence(filepath=settings.PERSISTANCE_PATH))
            .build()
        )
        app.add_handlers([HANDLERS])
        return app

    async def _manage_webhook(self) -> None:
        """Управляет вебхуком или переключает на режим опроса."""
        if settings.WEBHOOK_MODE:
            await self._app.bot.set_webhook(
                url=settings.WEBHOOK_URL,
                secret_token=settings.WEBHOOK_SECRET_KEY,
                allowed_updates=["message", "callback_query"],
            )
            logger.info(f"Webhook set up at {settings.WEBHOOK_URL}")
        else:
            await self._app.bot.delete_webhook()
            await self._app.updater.start_polling()
            logger.info("Polling started")

    async def _start_bot(self) -> None:
        """Запускает основное ASGI-приложение."""
        await self._app.start()

    async def _stop_bot(self) -> None:
        """Останавливает основное ASGI-приложение."""
        await Application.stop(self._app)
