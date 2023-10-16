from bot.factories import create_student
from bot.utils.filldb_command import CommandCreateObjects as BaseCommand


class Command(BaseCommand):
    """Создание профиля студент."""

    def _generate(self, amount: int):
        create_student(amount)
