from api_slackbot import cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete preprocessing temp leave request from the days before"

    def handle(self, *args, **kwargs):
        """
        Delete preprocessing temp leave request from the days before at begin shift time every morning
        """
        try:
            cron_tab.delete_temp_leave_request()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
