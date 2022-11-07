import api_user_lunch.cron_tab as cron_tab
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set lunch auto for user set auto_booking_lunch=True"

    def handle(self, *args, **kwargs):
        """
        Set lunch auto for user set auto_booking_lunch=True
        """
        try:
            cron_tab.set_lunch_auto_next_month()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
