import uuid

from api_base.models import TimeStampedModel
from api_user.models.profile import Profile
from api_workday.models.leave_type import LeaveType
from django.db import models


class RequestOff(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, default="Pending")
    reason = models.CharField(max_length=255, null=True, blank=True)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    total = models.FloatField(default=0)

    class Meta:
        db_table = "hr_request_off"
