from api_user.models.roles import Role
from core.settings.base import DEFAULT_SCOPES
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create mock data"

    def handle(self, *args, **kwargs):
        """
        Insert mock data
        """
        try:
            # Role
            Role.objects.get_or_create(
                name="Staff",
                description="Staff of Paradox",
                scope=" ".join(DEFAULT_SCOPES.keys()),
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
