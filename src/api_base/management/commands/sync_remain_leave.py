import api_workday.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Synchronized remain leave with date off for all users"

    def handle(self, *args, **kwargs):
        """
        synchronized table remain leave with date off for all system
        """
        try:
            cron_tab.sync_remain_leave()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
