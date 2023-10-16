from django.core.management.base import BaseCommand, CommandParser


class CommandCreateObjects(BaseCommand):
    """Шаблон для создания консольных команд заполнения БД."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргумент количества создаваемых объектов."""
        parser.add_argument(
            "--amount", type=int, help="Необходимое количество объектов."
        )

    def handle(self, *args, **options):
        """Реализация."""
        self._generate(options.get("amount"))
