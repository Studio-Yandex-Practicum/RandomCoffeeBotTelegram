from unittest.mock import AsyncMock, Mock

import pytest
from django.conf import settings
from telegram import InlineKeyboardButton

from bot.models import Student, Profession, Recruiter
from bot.utils.pagination import InlineKeyboardPaginator


@pytest.fixture
def update():
    """Update object fixture for telegram handlers."""
    return AsyncMock()


@pytest.fixture
def context():
    """Context object fixture for telegram handlers."""
    context = AsyncMock()
    context.bot = AsyncMock()
    context.bot.set_my_commands = AsyncMock(return_value=[])
    context.bot.set_chat_menu_button = AsyncMock(return_value=[])
    return context


@pytest.fixture
def mocked_reply_markup():
    """Reply markup mock."""
    return AsyncMock(return_value=[])


@pytest.fixture
def mocked_message_text():
    """Message text mock."""
    return "MESSAGE"


@pytest.fixture
def mocked_message(mocked_message_text):
    """Message object mock."""
    message = Mock()
    message.text = mocked_message_text
    return message


@pytest.fixture
def async_mocked_reply_markup():
    """Message object mock."""
    return AsyncMock(return_value=[])


@pytest.fixture
async def profession(db):
    """Profession object."""
    return await Profession.objects.acreate(name="prof-1")


@pytest.fixture
async def student(db, profession):
    """Student object."""
    return await Student.objects.acreate(
        telegram_id=1,
        name="student-1",
        telegram_username="student-username-1",
        profession=await profession,
    )


@pytest.fixture
async def recruiter(db):
    """Student object."""
    return await Recruiter.objects.acreate(
        telegram_id=1,
        name="recruiter-1",
        telegram_username="recruiter-username-1",
    )


@pytest.fixture
async def pagination_keyboard():
    """InlineKeyboardPaginator object."""
    telegram_paginator = InlineKeyboardPaginator(settings.DEFAULT_PAGE)
    telegram_paginator.add_before(
        InlineKeyboardButton(
            text="prof-1",
            callback_data="profession_prof-1",
        )
    )
    return telegram_paginator


@pytest.fixture
def mocked_pagination_reply_markup():
    """Reply markup pagination."""
    return '{"inline_keyboard": [[{"callback_data": "profession_prof-1", "text": "prof-1"}]]}'
