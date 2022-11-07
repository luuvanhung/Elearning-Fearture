import uuid

from api_base.models import TimeStampedModel
from api_user.models import Profile
from api_workday.models.request_off import RequestOff
from django.db import models


class RequestDetail(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    comment = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    request_off = models.ForeignKey(
        RequestOff, on_delete=models.CASCADE, related_name="request_detail"
    )
    approve = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="approve_id"
    )

    def __str__(self):
        return self.approve.name

    class Meta:
        db_table = "hr_request_detail"
