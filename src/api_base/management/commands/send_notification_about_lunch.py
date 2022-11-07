import api_user_lunch.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send information about lunch=True"

    def handle(self, *args, **kwargs):
        """
        Send information about lunch=True
        """
        try:
            cron_tab.send_notification_about_lunch()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
