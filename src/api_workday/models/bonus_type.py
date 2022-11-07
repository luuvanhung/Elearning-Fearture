import uuid

from api_base.models import TimeStampedModel
from django.db import models


class BonusType(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    name = models.CharField(max_length=255, default="", unique=True)
    descriptions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hr_bonus_type"
        ordering = ["-created_at"]
