import uuid

from api_base.models import TimeStampedModel
from api_probation.models import Probation
from django.db import models


class ProbationReminder(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    reminder_date = models.DateField(null=True, blank=True)
    probation = models.ForeignKey(
        Probation, related_name="reminders", on_delete=models.CASCADE
    )
    reminder_status = models.BooleanField(default=False)
    calendar_id = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        db_table = "hr_probation_reminder"
        ordering = ["-created_at"]
