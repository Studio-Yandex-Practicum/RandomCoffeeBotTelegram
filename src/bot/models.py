from django.db import models


class PracticumUser(models.Model):
    """Базовая модель для пользователей."""


class Student(PracticumUser):
    """Модель для студентов."""


class Recruter(PracticumUser):
    """Модель для рекрутеров."""


class CustomPair(models.Model):
    """Базовая модель для создания пар."""


class CreatedPair(CustomPair):
    """Модель для создания пары."""


class PassedPair(CustomPair):
    """Модель созвона."""
