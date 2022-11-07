import datetime
import uuid

from api_base.models import TimeStampedModel
from api_user.models.profile import Profile
from api_workday.managers.remain_leave import RemainLeaveManager
from django.db import models


class RemainLeave(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    year = models.IntegerField(default=datetime.datetime.now().year)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    annual_leave = models.FloatField(default=0)
    annual_leave_last_year = models.FloatField(default=0)
    current_days_off = models.FloatField(default=0)
    objects = RemainLeaveManager()

    class Meta:
        db_table = "hr_remain_year"
        ordering = ["-year"]
