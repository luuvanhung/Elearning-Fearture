import factory
from api_workday.models import RemainLeave
from faker import Factory

faker = Factory.create()


class RemainLeaveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RemainLeave
        django_get_or_create = ("year", "annual_leave", "current_days_off", "profile")

    year = "2020"
    annual_leave = 3
    current_days_off = 3
