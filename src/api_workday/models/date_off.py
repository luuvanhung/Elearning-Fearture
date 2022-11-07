import uuid

from api_base.models import TimeStampedModel
from api_workday.models.request_off import RequestOff
from common.constants.workday_constants import Workday
from django.db import models


class DateOff(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    date = models.DateField(null=True)
    type = models.CharField(max_length=255, null=True, default=Workday.FULL)
    lunch = models.BooleanField(default=False)
    request_off = models.ForeignKey(
        RequestOff, on_delete=models.CASCADE, related_name="date_off"
    )

    class Meta:
        db_table = "hr_date_off"
        ordering = ["-date"]
