import api_workday.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send notification to slack report whose left company today"

    def handle(self, *args, **kwargs):
        """
        Call function get total leave request today
        """
        try:
            cron_tab.get_leave_today()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
