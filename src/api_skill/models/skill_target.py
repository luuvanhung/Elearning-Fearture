from api_base.models import TimeStampedModel
from api_skill.models import SkillDefinition
from api_user.models import User
from django.db import models


class SkillTarget(TimeStampedModel):
    target_user = models.ForeignKey(
        User, related_name="skill_targets", on_delete=models.CASCADE
    )
    skill_definition = models.ForeignKey(
        SkillDefinition, related_name="skill_targets", on_delete=models.CASCADE
    )
    set_by_user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "hr_skill_targets"
        unique_together = ("target_user", "skill_definition")
