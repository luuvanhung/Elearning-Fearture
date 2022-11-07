from api_base.models import TimeStampedModel
from api_skill.models import SkillDefinition
from api_user.models import User
from django.db import models


class SkillVote(TimeStampedModel):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_user = models.ForeignKey(
        User, related_name="skill_votes", on_delete=models.CASCADE
    )
    skill_definition = models.ForeignKey(
        SkillDefinition, related_name="skill_votes", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "hr_skill_votes"
        unique_together = ("voter", "voted_user", "skill_definition")
