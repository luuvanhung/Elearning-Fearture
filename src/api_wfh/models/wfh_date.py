import uuid

from api_base.models import TimeStampedModel
from api_wfh.models.wfh_request import WfhRequest
from django.db import models


class WfhDate(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    date = models.DateField(null=True)
    lunch = models.BooleanField(default=False)
    wfh_request = models.ForeignKey(
        WfhRequest, on_delete=models.CASCADE, related_name="wfh_date"
    )

    class Meta:
        db_table = "hr_wfh_date"
        ordering = ["-date"]
