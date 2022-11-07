import uuid

from api_base.models import TimeStampedModel
from api_user.models.titles import Titles
from api_workday.models.leave_type_group import LeaveTypeGroup
from django.db import models


class LeaveType(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, null=True, unique=True)
    leave_type_group = models.ForeignKey(
        LeaveTypeGroup,
        related_name="leave_types",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    descriptions = models.TextField()
    is_active = models.BooleanField(default=True)
    is_count = models.BooleanField(default=True)
    days = models.IntegerField(default=1, null=True)
    approval_title = models.ForeignKey(
        Titles,
        related_name="leave_types",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "hr_leave_type"
        ordering = ["leave_type_group"]
