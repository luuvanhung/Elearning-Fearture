import uuid

from api_base.models import TimeStampedModel
from api_user.models.user import User
from django.db import models


class WfhRequest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    total = models.FloatField(default=0)

    class Meta:
        db_table = "hr_wfh_request"
