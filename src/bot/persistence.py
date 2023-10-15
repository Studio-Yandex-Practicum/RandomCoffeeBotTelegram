import json
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict

from loguru import logger
from redis.asyncio import Redis
from telegram.ext import BasePersistence
from telegram.ext._utils.types import ConversationDict


class RedisPersistence(BasePersistence):
    """Класс для использования Redis в боте."""

    def __init__(self, redis: Redis, on_flush: bool = False):
        """Инициализация объекта хранения данных в Redis."""
        super().__init__(update_interval=1)
        self.redis: Redis = redis
        self.on_flush = on_flush
        self.user_data: DefaultDict[int, dict] | None = None
        self.chat_data: DefaultDict[int, dict] | None = None
        self.bot_data: dict | None = None
        self.conversations: dict[str, dict[tuple, Any]] | None = None

    async def load_redis(self) -> None:
        """Загрузка всех данных из Redis."""
        try:
            data_str = await self.redis.get("TelegramBotPersistence")
            if data_str:
                data = json.loads(data_str)
                self.user_data = defaultdict(dict, data["user_data"])
                self.chat_data = defaultdict(dict, data["chat_data"])
                self.bot_data = data.get("bot_data", dict())
                self.conversations = data["conversations"]
            else:
                self.reset_data()
        except Exception as exc:
            self.reset_data()
            logger.error(f"Error loading data from Redis: {exc}")

    def reset_data(self) -> None:
        """Сброс всех данных в начальное состояние."""
        self.conversations = dict()
        self.user_data = defaultdict(dict)
        self.chat_data = defaultdict(dict)
        self.bot_data = dict()

    async def dump_redis(self) -> None:
        """Сохранение всех данных в Redis."""
        try:
            data = {
                "conversations": self.conversations,
                "user_data": self.user_data,
                "chat_data": self.chat_data,
                "bot_data": self.bot_data,
            }
            data_str = json.dumps(data)
            await self.redis.set("TelegramBotPersistence", data_str)
        except Exception as exc:
            logger.error(f"Error saving data to Redis: {exc}")

    async def update_and_dump(self, key: str, data: Any) -> None:
        """Обновление и сохранение конкретных данных в Redis."""
        try:
            data_str = json.dumps(data)
            await self.redis.hset("TelegramBotPersistence", key, data_str)
        except Exception as exc:
            logger.error(f"Error updating and saving {key} to Redis: {exc}")

    async def get_data(self, key: str) -> Any:
        """Получение конкретных данных из Redis."""
        try:
            data_str = await self.redis.hget("TelegramBotPersistence", key)
            if data_str:
                return json.loads(data_str)
            else:
                return None
        except Exception as exc:
            logger.error(f"Error getting {key} from Redis: {exc}")
            return None

    async def get_user_data(self) -> DefaultDict[int, dict[Any, Any]]:
        """Получение данных пользователя из Redis."""
        if not self.user_data:
            self.user_data = await self.get_data("user_data") or defaultdict(
                dict
            )
        return deepcopy(self.user_data)

    async def get_bot_data(self) -> DefaultDict[int, dict[Any, Any]]:
        """Получение данных бота из Redis."""
        if not self.bot_data:
            self.bot_data = await self.get_data("bot_data") or {}
        return deepcopy(self.bot_data)

    async def get_chat_data(self) -> DefaultDict[int, dict[Any, Any]]:
        """Получение данных чата из Redis."""
        if not self.chat_data:
            self.chat_data = await self.get_data("chat_data") or defaultdict(
                dict
            )
        return deepcopy(self.chat_data)

    async def get_conversations(self, name: str) -> ConversationDict:
        """Получение данных о разговорах из Redis."""
        if not self.conversations:
            self.conversations = await self.get_data("conversations") or {}
        return self.conversations.get(name, {}).copy()

    async def update_user_data(
        self, user_id: int, data: dict[Any, Any]
    ) -> None:
        """Обновление данных пользователя и сохранение в Redis."""
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            await self.update_and_dump("user_data", self.user_data)

    async def update_bot_data(self, data: dict) -> None:
        """Обновление данных бота и сохранение в Redis при необходимости."""
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            await self.update_and_dump("bot_data", self.bot_data)

    async def update_chat_data(self, chat_id: int, data: dict) -> None:
        """Обновление данных чата и сохранение в Redis."""
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            await self.update_and_dump("chat_data", self.chat_data)

    async def update_conversation(
        self, name: str, key: tuple[int, ...], new_state: object | None
    ) -> None:
        """Обновление данных разговора и сохранение в Redis."""
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            await self.update_and_dump("conversations", self.conversations)

    async def flush(self) -> None:
        """Принудительное сохранение всех данных в Redis."""
        await self.dump_redis()

    async def drop_user_data(self, user_id: int) -> None:
        """Не используется."""
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        """Не используется."""
        pass

    async def get_callback_data(self) -> Any | None:
        """Не используется."""
        pass

    async def refresh_bot_data(self, bot_data) -> None:
        """Не используется."""
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: Any) -> None:
        """Не используется."""
        pass

    async def refresh_user_data(self, user_id: int, user_data: Any) -> None:
        """Не используется."""
        pass

    async def update_callback_data(self, data: Any) -> None:
        """Не используется."""
        pass
