import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template_overall_comment import (
    EvaluationTemplateOverallComment,
)
from django.db import models


class EvaluationTemplateOverallCommentAssessorRole(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    overall_comment = models.ForeignKey(
        EvaluationTemplateOverallComment,
        related_name="assessor_roles",
        on_delete=models.CASCADE,
    )
    overall_comment_role = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "hr_evaluation_template_overall_comment_assessor_role"
        ordering = ["created_at"]
