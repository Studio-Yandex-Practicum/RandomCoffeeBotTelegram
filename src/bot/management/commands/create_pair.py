from django.core.management.base import BaseCommand, CommandParser

from ...factories import create_pair


class Command(BaseCommand):
    """Создание тестовой пары студент-рекрутер."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргумент количества создаваемых пар."""
        parser.add_argument(
            "--amount", type=int, help="Необходимое количество пар."
        )

    def _generate_pair(self, amount: int):
        """Создание пары студент-рекрутер."""
        create_pair(amount)

    def handle(self, *args, **options):
        """Реализация."""
        self._generate_pair(options.get("amount"))
