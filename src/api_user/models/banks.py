from api_base.models import TimeStampedModel
from django.db import models


class Banks(TimeStampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "hr_banks"

    def __repr__(self):
        return self.bank_name
