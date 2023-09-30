import asyncio
import logging
from typing import Self

from django.conf import settings
from telegram import BotCommand
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from bot.constants.commands import (
    HELP_COMMAND,
    HELP_DESCRIPTION,
    START_COMMAND,
    START_DESCRIPTION,
    SUPPORT_COMMAND,
    SUPPORT_DESCRIPTION,
)
from bot.constants.patterns import (
    CHANGE_NAME_PATTERN,
    CONTINUE_NAME_PATTERN,
    GO_PATTERN,
    NEXT_TIME_PATTERN,
    PARTICIPATE_PATTERN,
    PROFESSION_CHOICE_PATTERN,
    PROFILE_PATTERN,
    RESTART_PATTERN,
    ROLE_CHOICE_PATTERN,
    TO_SUPPORT_PATTERN,
)
from bot.constants.states import States
from bot.handlers.command_handlers import (
    help_handler,
    redirection_to_support,
    start_handler,
    support_bot_handler,
)
from bot.handlers.conversation_handlers import (
    change_name,
    continue_name,
    go,
    next_time,
    profession_choice,
    profile,
    restart_callback,
    role_choice,
    set_new_name,
    set_phone_number,
)

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
        await self.set_bot_commands()
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
        main_handler = await build_main_handler()
        app.add_handlers([main_handler, help_handler, support_bot_handler])
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

    async def set_bot_commands(self) -> None:
        """Установить команды бота и их описание для кнопки Menu."""
        commands: list[BotCommand] = [
            BotCommand(START_COMMAND, START_DESCRIPTION),
            BotCommand(HELP_COMMAND, HELP_DESCRIPTION),
            BotCommand(SUPPORT_COMMAND, SUPPORT_DESCRIPTION),
        ]

        await self._app.bot.set_my_commands(commands)


async def build_main_handler():
    """Функция создания главного обработчика."""
    return ConversationHandler(
        entry_points=[start_handler],
        persistent=True,
        name="main_handler",
        states={
            States.START: [
                CallbackQueryHandler(go, pattern=GO_PATTERN),
                CallbackQueryHandler(next_time, pattern=NEXT_TIME_PATTERN),
            ],
            States.HELP: [
                CallbackQueryHandler(
                    restart_callback, pattern=PARTICIPATE_PATTERN
                ),
                CallbackQueryHandler(
                    redirection_to_support, pattern=TO_SUPPORT_PATTERN
                ),
            ],
            States.ROLE_CHOICE: [
                CallbackQueryHandler(role_choice, pattern=ROLE_CHOICE_PATTERN)
            ],
            States.NEXT_TIME: [
                start_handler,
                CallbackQueryHandler(
                    restart_callback, pattern=RESTART_PATTERN
                ),
            ],
            States.PROFESSION_CHOICE: [
                CallbackQueryHandler(
                    profession_choice, pattern=PROFESSION_CHOICE_PATTERN
                )
            ],
            States.PROFILE: [
                CallbackQueryHandler(profile, pattern=PROFILE_PATTERN)
            ],
            States.SET_NAME: [
                CallbackQueryHandler(
                    continue_name, pattern=CONTINUE_NAME_PATTERN
                ),
                CallbackQueryHandler(change_name, pattern=CHANGE_NAME_PATTERN),
            ],
            States.SET_NEW_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_new_name)
            ],
            States.SET_PHONE_NUMBER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, set_phone_number
                )
            ],
        },
        fallbacks=[help_handler, start_handler],
    )
