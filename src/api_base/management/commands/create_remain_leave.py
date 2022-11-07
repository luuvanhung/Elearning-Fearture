import api_workday.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create remain leave for user in company next year"

    def handle(self, *args, **kwargs):
        """
        Create remain leave for user in company next year
        """
        try:
            cron_tab.create_remain_leave_for_next_year()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
