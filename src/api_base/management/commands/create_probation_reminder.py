import api_probation.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create probation reminder"

    def handle(self, *args, **kwargs):
        """
        Create probation reminder
        """
        try:
            cron_tab.get_probation_reminder_today()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
