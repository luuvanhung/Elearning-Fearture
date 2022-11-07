import uuid

from api_base.models import TimeStampedModel
from api_office.models import Office
from api_probation.models.evaluation_template_type import EvaluationTemplateType
from django.db import models


class EvaluationTemplate(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    office = models.ForeignKey(
        Office, related_name="evaluation_templates", on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        EvaluationTemplateType,
        default=None,
        related_name="evaluation_templates",
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, null=False)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "hr_evaluation_template"
