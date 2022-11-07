from api_base.models import TimeStampedModel
from api_skill.models import Skill, SkillLevel
from django.db import models


class SkillDefinition(TimeStampedModel):
    skill = models.ForeignKey(
        Skill, related_name="definitions", on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        SkillLevel, related_name="definitions", on_delete=models.CASCADE
    )
    requirements = models.TextField(null=True)

    class Meta:
        db_table = "hr_skill_definitions"
        unique_together = ("skill", "level")
        ordering = ["skill"]
