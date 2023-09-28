import datetime

from factory import Faker, LazyFunction, LazyAttributeSequence, Sequence, SubFactory
from factory.django import DjangoModelFactory

from .models import Profession, Recruiter, Student


class ProfessionFactory(DjangoModelFactory):
    """Профессия Model Factory."""

    class Meta:
        """Профессия для ProfessionFactory."""

        model = Profession

    name = Faker("job", locale="ru_RU")


class RecruterFactory(DjangoModelFactory):
    """Рекрутер Model Factory."""

    class Meta:
        """Метакласс для RecruterFactory."""

        model = Recruiter

    telegram_id = Sequence(lambda n: '1%08d' % n)
    name = Faker("first_name", locale="ru_RU")
    surname = Faker("first_name", locale="ru_RU")
    telegram_username = LazyAttributeSequence(lambda obj, n: '@%s' % (obj.name, n))
    registration_date = LazyFunction(datetime.datetime.now)
    last_login_date =  LazyFunction(datetime.datetime.now)


class StudentFactory(DjangoModelFactory):
    """Студент Model Factory."""

    class Meta:
        """Метакласс для StudentrFactory."""

        model = Student

    telegram_id = Sequence(lambda n: '2%08d' % n)
    name = Faker("first_name", locale="ru_RU")
    surname = Faker("first_name", locale="ru_RU")
    telegram_username = LazyAttributeSequence(lambda obj, n: '@%s' % (obj.name, n))
    registration_date = LazyFunction(datetime.datetime.now)
    last_login_date =  LazyFunction(datetime.datetime.now)
    profession = SubFactory(RecruterFactory)
