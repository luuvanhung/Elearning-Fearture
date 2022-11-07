from api_base.models import TimeStampedModel
from api_skill.models import SkillDefinition
from api_user.models import Titles, User
from django.db import models


class TitleSkill(TimeStampedModel):
    title = models.ForeignKey(
        Titles, related_name="title_skills", on_delete=models.SET_NULL, null=True
    )
    skill_definition = models.ForeignKey(
        SkillDefinition, related_name="title_skills", on_delete=models.CASCADE
    )
    set_by_user = models.ForeignKey(
        User,
        related_name="title_skills",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "hr_title_skill"
        unique_together = ("title", "skill_definition")
