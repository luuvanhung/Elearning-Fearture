from api_oauth2.models import ApiKey
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create api key"

    def add_arguments(self, parser):
        parser.add_argument("name", nargs="+", type=str)
        parser.add_argument("scope", nargs="+", type=str)
        parser.add_argument("application_id", nargs="+", type=int)

    def handle(self, *args, **options):
        api_key, key = ApiKey.objects.create_key(
            name=options["name"][0],
            scope=options["scope"][0],
            application_id=options["application_id"][0],
        )
        self.stdout.write(self.style.SUCCESS('Successfully create api key "%s"' % key))
