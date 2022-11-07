# Generated by Django 3.2.3 on 2022-07-21 09:51

from django.db import migrations


def initial_bonus_type(apps, schema_editor):
    bonus_type_model = apps.get_model("api_workday", "BonusType")
    queryset = bonus_type_model.objects.all()
    bonus_types = []

    bonus_type_overtime = bonus_type_model(name="Overtime")
    bonus_type_other = bonus_type_model(name="Bonus")
    bonus_types.extend([
        bonus_type_overtime,
        bonus_type_other
    ])
    bonus_type_model.objects.bulk_create(bonus_types)


class Migration(migrations.Migration):

    dependencies = [
        ('api_workday', '0004_initial_bonus_leaves'),
    ]

    operations = [
        migrations.RunPython(initial_bonus_type, migrations.RunPython.noop)
    ]