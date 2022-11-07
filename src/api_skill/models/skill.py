from api_base.models import TimeStampedModel
from django.db import models


class Skill(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "hr_skills"
