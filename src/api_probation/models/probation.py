import uuid

from api_base.models import TimeStampedModel
from api_probation.models.evaluation_template import EvaluationTemplate
from api_team.models import Team
from api_user.models import User
from django.db import models


class Probation(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    employee = models.ForeignKey(
        User, related_name="probations", on_delete=models.CASCADE
    )
    probation_line_manager = models.ForeignKey(
        User,
        related_name="probation_line_manager",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        Team,
        related_name="probations",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    probation_end_date = models.DateField(null=True, blank=True)
    self_evaluation_end_date = models.DateField(null=True, blank=True)
    signing_official_labor_contract = models.BooleanField(default=False, blank=True)
    labor_contract_term = models.CharField(max_length=255, null=True, blank=True)
    other_actions_and_updates = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    evaluation_template = models.ForeignKey(
        EvaluationTemplate, related_name="probations", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "hr_probation"
        ordering = ["-created_at"]
