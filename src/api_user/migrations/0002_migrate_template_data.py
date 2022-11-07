# Generated by Django 2.2.7 on 2020-09-15 02:46
import datetime

from common.constants.user_constants import BankConstant, TitleConstant
from core.settings.base import SECRET_KEY, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from django.contrib.auth.hashers import make_password
from django.db import migrations, transaction


def load_banks(apps, schema_editor):
    banks = []
    bank_model = apps.get_model("api_user", "Banks")
    for bank_name in BankConstant.BANKS:
        banks.append(bank_model(name=bank_name[0]))
    bank_model.objects.bulk_create(banks)


def load_titles(apps, schema_editor):
    title_model = apps.get_model("api_user", "Titles")
    weight = 100
    titles = []
    for title in TitleConstant.get_title_list():
        titles.append(title_model(title=title, weight=weight))
        weight -= 1
    title_model.objects.bulk_create(titles)


def add_users_and_role(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("api_user", "User")
    Profile = apps.get_model("api_user", "Profile")
    Role = apps.get_model("api_user", "Role")
    Office = apps.get_model("api_office", "Office")
    RemainLeave = apps.get_model("api_workday", "RemainLeave")

    admin_role, created = Role.objects.get_or_create(
        name="Super Administrator",
        description="Unlimited resources access.",
        scope="__all__",
    )
    admin_user = User.objects.filter(is_superuser=True).exists()
    office = Office.objects.all().first()
    if not admin_user:
        with transaction.atomic():
            admin_user = User()
            admin_user.email = (
                SUPER_ADMIN_EMAIL  # Todo: Get the value from environment vairable
            )
            admin_user.password = make_password(
                SUPER_ADMIN_PASSWORD, salt=SECRET_KEY
            )  # Todo: Get the value from environment vairable
            admin_user.staff = True
            admin_user.admin = True
            admin_user.active = True
            admin_user.is_superuser = True
            admin_user.save()
            profile = Profile.objects.create(
                user=admin_user,
                name="Super Administrator",
                office=office,
                maximum_level_approved=0,
                personal_email=admin_user.email,
            )
            RemainLeave.objects.create(
                year=datetime.datetime.now().year,
                annual_leave=12,
                current_days_off=12,
                profile=profile,
            )
    # add default admin scope
    admin_user = User.objects.filter(email=SUPER_ADMIN_EMAIL).first()
    if not admin_user:
        return
    admin_user.roles.add(admin_role)
    admin_user.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [("api_user", "0001_initial"), ("api_workday", "0001_initial")]

    operations = [
        migrations.RunPython(load_banks, migrations.RunPython.noop),
        migrations.RunPython(load_titles, migrations.RunPython.noop),
        migrations.RunPython(add_users_and_role, migrations.RunPython.noop),
    ]
