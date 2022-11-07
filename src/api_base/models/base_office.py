from api_base.models import TimeStampedModel
from django.db import models


class BaseOffice(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        abstract = True
