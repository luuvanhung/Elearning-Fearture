import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template import EvaluationTemplate
from django.db import models


class EvaluationTemplateCompetence(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    evaluation_template = models.ForeignKey(
        EvaluationTemplate, related_name="competencies", on_delete=models.CASCADE
    )
    competence = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hr_evaluation_template_competence"
        ordering = ["created_at"]
