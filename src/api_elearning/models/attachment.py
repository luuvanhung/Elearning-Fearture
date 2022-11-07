import uuid

from api_base.models import TimeStampedModel
from api_elearning.models import Lesson
from api_user.models import User
from django.db import models

# def file_name(instance, filename):
#     # end_path = str(instance.id) + '.' + filename.split('.')[-1]
#     # final_path = "/".join(
#     #     ['courses', str(instance.lesson.chapter.course.id), 'chapters', str(instance.lesson.chapter.id), 'lessons',
#     #      str(instance.lesson.id), 'responser', str(instance.responser.id), str(end_path)])
#
#     return final_path

def upload_path(instance, filename):
    return instance.path


class Attachment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    path = models.CharField(default=None, null=True, max_length=255)
    file = models.FileField(
        upload_to=upload_path, max_length=255, blank=True, null=True
    )
    mine_type = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name="attachments")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="attachments")
    original_name = models.CharField(max_length=255)
    length = models.IntegerField(default=0)
    forced_read = models.BooleanField(default=False)

    class Meta:
        db_table = "el_attachments"
        ordering = ["-created_at"]
