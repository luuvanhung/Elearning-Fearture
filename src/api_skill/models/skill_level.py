from api_base.models import TimeStampedModel
from django.db import models


class SkillLevel(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    weight = models.IntegerField(unique=True)

    class Meta:
        db_table = "hr_skill_levels"
