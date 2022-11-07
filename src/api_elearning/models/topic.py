import uuid

from api_base.models import TimeStampedModel
from django.db import models


class Topic(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "el_topics"
        ordering = ["-created_at"]
