from bot.factories import create_pair
from bot.utils.filldb_command import CommandCreateObjects as BaseCommand


class Command(BaseCommand):
    """Создание тестовой пары студент-рекрутер."""

    def _generate(self, amount: int):
        create_pair(amount)
