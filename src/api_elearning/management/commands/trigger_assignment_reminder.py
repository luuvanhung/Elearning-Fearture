from django.core.management.base import BaseCommand
import api_elearning.cron_tab as cron_tab


class Command(BaseCommand):
    help = "Send assignment reminder to whom have not finished their training"

    def handle(self, *args, **kwargs):
        """
        Call function to trigger assignment reminder
        """
        try:
            cron_tab.send_assignments_reminder()
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
