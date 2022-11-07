import uuid

from django.db import models

from api_base.models import TimeStampedModel
from api_elearning.models import Topic
from api_user.models import User
from django.db import models


def name_file(instance, filename):
    return "/".join([str(instance.id), filename])


class Course(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    short_des = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='instructor_courses', default=None)
    cover_image = models.FileField(upload_to=name_file, blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True, null=True, related_name="courses")
    last_modifier = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="modify_courses", default=None)

    class Meta:
        db_table = "el_courses"
        ordering = ["-created_at"]
