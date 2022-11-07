import uuid

from django.db import models

from api_base.models import TimeStampedModel
from api_elearning.models import Course
from api_user.models import User


class Chapter(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    previous_chapter = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    last_modifier = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="modify_chapters", default=None)

    class Meta:
        db_table = "el_chapters"
        ordering = ["created_at"]
