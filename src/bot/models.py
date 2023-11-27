from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from bot.utils.transliteration import transliteration
from bot.utils.validators import validator_message_key


class Profession(models.Model):
    """Модель для хранения профессий."""

    name = models.CharField(
        max_length=128, unique=True, verbose_name="Название профессии"
    )
    professional_key = models.CharField(
        max_length=128, unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"

    def __str__(self):
        return self.name


@receiver(pre_save)
def create_key(sender, instance, *args, **kwargs) -> None:
    """Save transliterate field from 'name' into 'professional_key'."""
    if hasattr(sender, "professional_key"):
        instance.professional_key = transliteration(
            instance.name, prefix="profession_"
        )


class PracticumUser(models.Model):
    """Базовая модель для пользователей."""

    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
        null=True,
    )
    telegram_id = models.BigIntegerField(
        primary_key=True,
        verbose_name="Telegram User ID",
    )
    telegram_username = models.CharField(
        max_length=255,
        verbose_name="Ник телеграма или номер телефона",
        unique=True,
    )
    has_pair = models.BooleanField(default=False, verbose_name="Есть пара")
    search_start_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Время начала поиска",
    )
    last_login_date = models.DateField(
        auto_now=True, verbose_name="Заходил в последний раз"
    )
    registration_date = models.DateField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.telegram_username} | id: {self.telegram_id}"


class ItSpecialist(PracticumUser):
    """Модель для IT-специалистов."""

    profession = models.ForeignKey(
        Profession,
        related_name="itspecialists",
        on_delete=models.PROTECT,
        verbose_name="Профессия",
    )

    class Meta:
        verbose_name = "IT-специалист"
        verbose_name_plural = "IT-специалисты"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Recruiter(PracticumUser):
    """Модель для рекрутеров."""

    class Meta:
        verbose_name = "Рекрутер"
        verbose_name_plural = "Рекрутеры"

    def __str__(self):
        return f"{self.name} {self.surname}"


class CustomPair(models.Model):
    """Базовая модель для создания пар."""

    itspecialist = models.ForeignKey(
        ItSpecialist, on_delete=models.CASCADE, verbose_name="IT-специалист"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, verbose_name="Рекрутер"
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f"IT-специалист {self.itspecialist.telegram_username} | "
            f"Рекрутер {self.recruiter.telegram_username}"
        )


class CreatedPair(CustomPair):
    """Модель для создания пары."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["itspecialist"], name="unique_itspecialist"
            ),
            models.UniqueConstraint(
                fields=["recruiter"], name="unique_recruiter"
            ),
            models.UniqueConstraint(
                fields=["itspecialist", "recruiter"],
                name="unique_created_pair",
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
                fields=["itspecialist", "recruiter"], name="unique_passed_pair"
            )
        ]
        verbose_name = "Завершенная пара"
        verbose_name_plural = "Завершенные пары"


class FormUrl(models.Model):
    """Модель для ссылок на формы."""

    title = models.CharField(max_length=255, verbose_name="Название ссылки")
    url = models.URLField(verbose_name="Ссылка", null=True)
    url_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Ключ ссылки",
    )

    class Meta:
        verbose_name = "Ссылка на форму"
        verbose_name_plural = "Ссылки на формы"

    def __str__(self):
        return f"Название {self.title} | Ссылка {self.url}"


class MessageBot(models.Model):
    """Модель сообщений бота."""

    title = models.CharField(
        max_length=255, unique=True, verbose_name="Название сообщения бота"
    )
    message = models.TextField(
        unique=True,
        verbose_name="Текст сообщения бота",
        help_text=(
            "Не удаляйте '{}'. Это метка для вставки динамических данных."
        ),
    )
    message_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Ключ сообщения бота",
        validators=[validator_message_key()],
    )

    class Meta:
        verbose_name = "Сообщение бота"
        verbose_name_plural = "Сообщения бота"

    def __str__(self):
        return f"Название '{self.title}'"
