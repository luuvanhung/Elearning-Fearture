# Generated by Django 3.2.3 on 2022-08-18 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_workday', '0007_bonustype_descriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonusleave',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_user.profile'),
        ),
    ]
