import uuid

from api_base.models import TimeStampedModel
from django.db import models


class LeaveTypeGroup(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, unique=True, null=True)
    is_company_pay = models.BooleanField(default=True)
    is_insurance_pay = models.BooleanField(default=True)

    class Meta:
        db_table = "hr_leave_type_group"
        ordering = ["created_at"]
