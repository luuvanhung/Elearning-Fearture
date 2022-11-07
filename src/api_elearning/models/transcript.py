import uuid

from django.db import models

from api_base.models import TimeStampedModel
from api_elearning.models import Attachment


class Transcript(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    script_at_second = models.IntegerField()
    content = models.CharField(max_length=255)
    attachment = models.ForeignKey(Attachment, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="attachment_transcripts")

    class Meta:
        db_table = "el_transcripts"
        ordering = ["script_at_second"]
