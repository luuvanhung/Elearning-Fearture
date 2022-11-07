import datetime

from api_base.models import BaseOffice
from api_office.models import Group
from api_user.models import User
from django.db import models


class Office(BaseOffice):
    address = models.CharField(max_length=255, null=True, blank=True)
    manager = models.ForeignKey(
        User, related_name="office", on_delete=models.SET_NULL, null=True, blank=True
    )
    group = models.ForeignKey(
        Group, related_name="office", on_delete=models.CASCADE, null=True, blank=True
    )
    expired_annual_leave_last_year = models.IntegerField(
        null=True, blank=True, default=6
    )

    # detail information
    established_date = models.DateField(default=datetime.date.today)
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = "hr_offices"
