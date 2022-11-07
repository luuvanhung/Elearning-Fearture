import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template_competence import (
    EvaluationTemplateCompetence,
)
from django.db import models


class EvaluationTemplateCompetenceAssessorRole(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    evaluation_competence = models.ForeignKey(
        EvaluationTemplateCompetence,
        related_name="assessor_roles",
        on_delete=models.CASCADE,
    )
    assessor_role = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "hr_evaluation_template_competence_assessor_role"
        ordering = ["created_at"]
