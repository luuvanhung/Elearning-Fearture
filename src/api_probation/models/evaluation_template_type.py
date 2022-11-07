import uuid

from api_base.models import TimeStampedModel
from django.db import models


class EvaluationTemplateType(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    type_name = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "hr_evaluation_template_type"
