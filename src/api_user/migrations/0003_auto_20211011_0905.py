# Generated by Django 3.2.3 on 2021-10-11 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_user", "0002_migrate_template_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="lunch",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="lunch_weekly",
        ),
    ]