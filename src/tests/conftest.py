from unittest.mock import AsyncMock, Mock

import pytest

from bot.models import Student, Profession


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
