from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    """Модель для создания администраторов."""

    class Meta:
        ordering = ("id",)
        verbose_name = "AdminUser"
        verbose_name_plural = "AdminUsers"

    def __str__(self):
        return self.username
