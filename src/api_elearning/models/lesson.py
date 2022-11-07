import uuid

from django.db import models

from api_base.models import TimeStampedModel
from api_elearning.models import Chapter
from api_user.models import User


class Lesson(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons")
    last_modifier = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="modify_lessons", default=None)
    previous_lesson = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "el_lessons"
        ordering = ["created_at"]
