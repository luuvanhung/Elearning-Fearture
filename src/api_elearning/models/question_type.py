import uuid

from api_base.models import TimeStampedModel
from django.db import models


class QuestionType(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        db_table = "el_question_types"
        ordering = ["created_at"]
        unique_together = ('name',)
