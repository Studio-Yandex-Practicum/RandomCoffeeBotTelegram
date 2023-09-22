from django.db import models


class Profession(models.Model):
    """Модель для хранения профессий."""

    name = models.CharField(
        max_length=128, unique=True, verbose_name="Название профессии"
    )

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"

    def __str__(self):
        return self.name


class PracticumUser(models.Model):
    """Базовая модель для пользователей."""

    telegram_id = models.IntegerField(
        primary_key=True, verbose_name="Telegram User ID"
    )
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    telegram_username = models.CharField(
        max_length=255, verbose_name="Ник в телеграмме", unique=True
    )
    registration_date = models.DateField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    last_login_date = models.DateField(
        auto_now=True, verbose_name="Заходил в последний раз"
    )
    has_pair = models.BooleanField(default=False, verbose_name="Есть пара")
    waiting_time = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name="Время ожидания пары",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.telegram_username} | id: {self.telegram_id}"


class Student(PracticumUser):
    """Модель для студентов."""

    profession = models.ForeignKey(
        Profession,
        related_name="students",
        on_delete=models.PROTECT,
        verbose_name="Профессия",
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Recruiter(PracticumUser):
    """Модель для рекрутеров."""

    class Meta:
        verbose_name = "Рекрутер"
        verbose_name_plural = "Рекрутеры"


class CustomPair(models.Model):
    """Базовая модель для создания пар."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Студент"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, verbose_name="Рекрутер"
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f"Студент {self.student.telegram_username} | "
            f"Рекрутер {self.recruiter.telegram_username}"
        )


class CreatedPair(CustomPair):
    """Модель для создания пары."""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student"], name="unique_student"),
            models.UniqueConstraint(
                fields=["recruiter"], name="unique_recruiter"
            ),
            models.UniqueConstraint(
                fields=["student", "recruiter"], name="unique_created_pair"
            ),
        ]
        verbose_name = "Активная пара"
        verbose_name_plural = "Активные пары"


class PassedPair(CustomPair):
    """Модель созвона."""

    interview_successful = models.BooleanField(
        default=False, verbose_name="Встреча прошла успешно"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "recruiter"], name="unique_passed_pair"
            )
        ]
        verbose_name = "Завершенная пара"
        verbose_name_plural = "Завершенные пары"
