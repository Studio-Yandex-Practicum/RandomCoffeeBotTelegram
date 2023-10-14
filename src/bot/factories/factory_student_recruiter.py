from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from bot.models import Recruiter

LOW_LIMIT_NUMBER = 900000000
HIGH_LIMIT_NUMBER = 999999999


class RecruiterFactory(DjangoModelFactory):
    """The factory generates recruiters."""

    class Meta:
        model = Recruiter

    telegram_id = FuzzyInteger(LOW_LIMIT_NUMBER, HIGH_LIMIT_NUMBER)
    name = Faker("first_name")
    surname = Faker("last_name")
    telegram_username = Faker("user_name")
