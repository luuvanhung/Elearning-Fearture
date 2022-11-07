import uuid

from api_user.models import Profile
from django.db import models
from django.utils import timezone


class UserLunch(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    date = models.DateField(null=True, default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    has_veggie = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date

    class Meta:
        db_table = "hr_user_lunch"
        ordering = ["-created_at"]
