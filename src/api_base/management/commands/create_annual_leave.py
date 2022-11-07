import api_workday.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add annual leave for user in company"

    def handle(self, *args, **kwargs):
        """
        Add annual leave for user in company
        """
        try:
            cron_tab.add_annual_leave()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
