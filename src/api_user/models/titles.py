from api_base.models import TimeStampedModel
from django.db import models


class Titles(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "hr_titles"

    def __repr__(self):
        return self.title
