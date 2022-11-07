from django.db import migrations


def add_authentication_provider(apps, schema_editor):
    AuthenticationProvider = apps.get_model(
        "api_authservices", "AuthenticationProvider"
    )
    exist_authentication_provider = AuthenticationProvider.objects.filter(
        service_name="accounts.google.com"
    ).exists()
    if not exist_authentication_provider:
        AuthenticationProvider.objects.create(service_name="accounts.google.com")


class Migration(migrations.Migration):
    dependencies = [
        ("api_authservices", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(add_authentication_provider, migrations.RunPython.noop)
    ]
