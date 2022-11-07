# Generated by Django 3.2.3 on 2022-09-25 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_office', '0005_squad'),
        ('api_team', '0004_alter_team_team_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='squad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='api_office.squad'),
        ),
    ]
