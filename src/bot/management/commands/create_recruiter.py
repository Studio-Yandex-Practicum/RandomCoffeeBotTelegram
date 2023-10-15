from django.core.management.base import BaseCommand, CommandParser

from ...factories import create_recruiter


class Command(BaseCommand):
    """Создание тестового профиля рекрутера."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргумент количества создаваемых профилей."""
        parser.add_argument(
            "--amount", type=int, help="Необходимое количество профилей."
        )

    def _generate_recruiter(self, amount: int):
        """Создание профилей рекрутеров."""
        create_recruiter(amount)

    def handle(self, *args, **options):
        """Реализация."""
        self._generate_recruiter(options.get("amount"))
