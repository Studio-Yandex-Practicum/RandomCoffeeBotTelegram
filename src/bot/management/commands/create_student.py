from django.core.management.base import BaseCommand, CommandParser

from ...factories import create_student


class Command(BaseCommand):
    """Создание тестового профиля студента."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргумент количества создаваемых профилей."""
        parser.add_argument(
            "--amount", type=int, help="Необходимое количество профилей."
        )

    def _generate_students(self, amount: int):
        """Создание профилей студентов."""
        create_student(amount)

    def handle(self, *args, **options):
        """Реализация."""
        self._generate_students(options.get("amount"))
