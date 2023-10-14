from django.core.management.base import BaseCommand, CommandParser

from bot.factories.factory_student_recruiter import RecruiterFactory


class Command(BaseCommand):
    """Generate fake data for models."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Add parameter amount for fake data."""
        parser.add_argument("--amount", type=int, help="The amount fake data.")

    def _generate_recruiters(self, amount: int):
        RecruiterFactory.create_batch(amount)

    def handle(self, *args, **options):
        """Realization."""
        self._generate_recruiters(options.get("amount"))
