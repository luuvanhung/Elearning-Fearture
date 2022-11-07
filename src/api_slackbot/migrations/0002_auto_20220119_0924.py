# Generated by Django 3.2.3 on 2022-01-19 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_user", "0003_auto_20211011_0905"),
        ("api_slackbot", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="templeaverequest",
            options={},
        ),
        migrations.RemoveField(
            model_name="templeaverequest",
            name="profile_id",
        ),
        migrations.AddField(
            model_name="templeaverequest",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api_user.profile",
            ),
        ),
        migrations.AddField(
            model_name="templeaverequest",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
