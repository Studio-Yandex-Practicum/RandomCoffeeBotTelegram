from random import choice

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from bot.models import (
    CreatedPair,
    ItSpecialist,
    PassedPair,
    Profession,
    Recruiter,
)

LOW_LIMIT_NUMBER = 900000000
HIGH_LIMIT_NUMBER = 999999999


class RecruiterFactory(DjangoModelFactory):
    """Фабрика профиля рекрутера для тестирования проекта."""

    class Meta:
        model = Recruiter

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    telegram_id = FuzzyInteger(LOW_LIMIT_NUMBER, HIGH_LIMIT_NUMBER)
    telegram_username = factory.Faker("user_name")
    registration_date = timezone.now()
    last_login_date = timezone.now()
    in_search_pair = False
    has_pair = False
    search_start_time = timezone.now()


class ItSpecialistFactory(RecruiterFactory):
    """Фабрика профиля IT-специалиста для тестирования проекта."""

    class Meta:
        model = ItSpecialist

    profession = factory.LazyFunction(lambda: choice(Profession.objects.all()))


class PairFactory(DjangoModelFactory):
    """Фабрика тестовой пары IT-специалист-рекрутёр."""

    class Meta:
        model = CreatedPair

    itspecialist = factory.SubFactory(ItSpecialistFactory, has_pair=True)
    recruiter = factory.SubFactory(RecruiterFactory, has_pair=True)
    date = timezone.now()


class PassedPairFactory(DjangoModelFactory):
    """Фабрика тестовой пары IT-специалист-рекрутёр, которая созвонилась."""

    class Meta:
        model = PassedPair

    interview_successful = True
    itspecialist = factory.SubFactory(ItSpecialistFactory)
    recruiter = factory.SubFactory(RecruiterFactory)
    date = timezone.now()


def create_itspecialist(amount: int = 1):
    """Создание профиля IT-специалиста для тестов программы."""
    ItSpecialistFactory.create_batch(amount)


def create_recruiter(amount: int = 1):
    """Создание профиля рекрутера для тестов программы."""
    RecruiterFactory.create_batch(amount)


def create_pair(amount: int = 1):
    """Создание тестовой пары IT-специалист-рекрутёр."""
    PairFactory.create_batch(amount)


def create_passedpair(amount: int = 1):
    """Создание тестовой пары IT-специалист-рекрутёр, которая созвонилась."""
    PassedPairFactory.create_batch(amount)
