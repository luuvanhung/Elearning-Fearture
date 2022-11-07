import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template_competence import (
    EvaluationTemplateCompetence,
)
from api_probation.models.evaluation_template_competence_assessor_role import (
    EvaluationTemplateCompetenceAssessorRole,
)
from api_probation.models.probation import Probation
from api_user.models import User
from django.db import models


class ProbationCompetence(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    employee = models.ForeignKey(
        User, related_name="probation_competencies", on_delete=models.CASCADE
    )
    probation = models.ForeignKey(
        Probation, related_name="competencies", on_delete=models.CASCADE
    )
    evaluation_template_competence = models.ForeignKey(
        EvaluationTemplateCompetence,
        related_name="probation_competencies",
        on_delete=models.CASCADE,
    )
    evaluation_template_competence_assessor_role = models.ForeignKey(
        EvaluationTemplateCompetenceAssessorRole,
        related_name="probation_competencies",
        on_delete=models.CASCADE,
    )
    assessor = models.ForeignKey(
        User,
        related_name="assessors_probation_competencies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    score = models.IntegerField(default=0)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hr_probation_competence"
        ordering = ["-created_at"]
