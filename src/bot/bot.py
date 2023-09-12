import asyncio
import logging

from django.conf import settings
from telegram.ext import Application, PicklePersistence

from .handlers import HANDLERS

logger = logging.getLogger(__name__)


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._app = None
        self._stop_event = asyncio.Event()
        logger.info('Bot instance created.')

    def start(self):
        logger.info('Bot starting...')
        self._stop_event.clear()
        asyncio.create_task(self._run())

    def stop(self):
        logger.info('Bot stopping...')
        self._stop_event.set()

    async def _run(self):
        self._app = await self._build_app()
        await self._app.initialize()
        await self._manage_webhook()
        await self._start_bot()
        await self._stop_event.wait()
        await self._stop_bot()

    async def _build_app(self):
        app = Application.builder().token(
            settings.TELEGRAM_TOKEN).persistence(
            PicklePersistence(filepath=settings.PERSISTANCE_PATH)
        ).build()
        app.add_handlers([HANDLERS])
        return app

    async def _manage_webhook(self):
        if settings.WEBHOOK_MODE:
            await self._app.bot.set_webhook(url=settings.WEBHOOK_URL)
            logger.info(f"Webhook set up at {settings.WEBHOOK_URL}")
        else:
            await self._app.bot.delete_webhook()
            await self._app.updater.start_polling()
            logger.info('Polling started')

    async def _start_bot(self):
        await self._app.start()

    async def _stop_bot(self):
        await self._app.updater.stop()
        await self._app.stop()
