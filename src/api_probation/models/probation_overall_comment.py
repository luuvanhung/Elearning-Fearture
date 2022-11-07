import uuid

from api_base.models import TimeStampedModel
from api_probation.models import Probation
from api_probation.models.evaluation_template_overall_comment import (
    EvaluationTemplateOverallComment,
)
from api_probation.models.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRole,
)
from api_user.models import User
from django.db import models


class ProbationOverallComment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    employee = models.ForeignKey(
        User, related_name="probation_comments", on_delete=models.CASCADE
    )
    probation = models.ForeignKey(
        Probation, related_name="overall_comments", on_delete=models.CASCADE
    )
    evaluation_template_overall_comment = models.ForeignKey(
        EvaluationTemplateOverallComment,
        related_name="probation_overall_comments",
        on_delete=models.CASCADE,
    )
    evaluation_template_overall_comment_assessor_role = models.ForeignKey(
        EvaluationTemplateOverallCommentAssessorRole,
        related_name="probation_overall_comments",
        on_delete=models.CASCADE,
    )
    assessor = models.ForeignKey(
        User,
        related_name="assessors_probation_comments",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    score = models.IntegerField(default=0)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hr_probation_overall_comment"
        ordering = ["-created_at"]
