from ...factories import create_recruiter
from ...utils.filldb_command import CommandCreateObjects as BaseCommand


class Command(BaseCommand):
    """Создание профиля рекрутер."""

    def _generate(self, amount: int):
        create_recruiter(amount)
