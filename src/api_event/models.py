import uuid

from api_user.models import Profile
from api_user.models.photo import name_file
from django.db import models
from django.utils import timezone


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    date = models.DateField(null=True, default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wishes = models.TextField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=name_file)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def image_attr(self):
        return self.image
