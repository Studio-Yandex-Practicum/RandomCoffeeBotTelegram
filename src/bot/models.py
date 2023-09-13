from django.db import models


class ProfessionChoice(models.TextChoices):
    """Класс для выбора профессий."""

    ANALYST = "AN", "Аналитик"
    BACKEND = "BA", "Бэкенд-разработчик"
    FRONTEND = "FR", "Фронтенд-разработчик"
    TESTER = "TE", "Тестировщик"


class PracticumUser(models.Model):
    """Базовая модель для пользователей."""

    user_id = models.IntegerField(primary_key=True, verbose_name="Telegram id")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    tg_username = models.CharField(
        max_length=255, verbose_name="Ник в телеграмме"
    )
    registration_date = models.DateField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    last_login_date = models.DateField(
        auto_now=True, verbose_name="Заходил в последний раз"
    )
    is_vacant = models.BooleanField(default=False, verbose_name="Есть пара")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.tg_username} | id: {self.user_id}"


class Student(PracticumUser):
    """Модель для студентов."""

    profession = models.CharField(
        max_length=2,
        choices=ProfessionChoice.choices,
        default=ProfessionChoice.ANALYST,
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
            f"Студент {self.student.tg_username} | "
            f"Рекрутер {self.recruiter.tg_username}"
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
        verbose_name = "Текущая пара"
        verbose_name_plural = "Текущие пары"


class PassedPair(CustomPair):
    """Модель созвона."""

    is_interview_successful = models.BooleanField(
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
