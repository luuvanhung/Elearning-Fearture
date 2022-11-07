# Generated by Django 3.2.3 on 2021-09-24 11:00

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("api_user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserLunch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "date",
                    models.DateField(default=django.utils.timezone.now, null=True),
                ),
                ("has_veggie", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api_user.profile",
                    ),
                ),
            ],
            options={
                "db_table": "hr_user_lunch",
                "ordering": ["-created_at"],
            },
        ),
    ]
