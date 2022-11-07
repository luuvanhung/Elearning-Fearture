import uuid

from api_base.models import TimeStampedModel
from api_user.models import Profile
from api_workday.models import BonusType
from django.db import models


class BonusLeave(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    reason = models.TextField(default="")
    bonus_days = models.FloatField(default=0.5)
    expired_at = models.DateTimeField(null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    bonus_type = models.ForeignKey(BonusType, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "hr_bonus_leave"
        ordering = ["-created_at"]
