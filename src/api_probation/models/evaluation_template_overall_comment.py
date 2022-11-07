import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template import EvaluationTemplate
from django.db import models


class EvaluationTemplateOverallComment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    evaluation_template = models.ForeignKey(
        EvaluationTemplate, related_name="overall_comments", on_delete=models.CASCADE
    )
    term = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "hr_evaluation_template_overall_comment"
        ordering = ["created_at"]
