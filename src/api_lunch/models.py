import uuid

from api_providers.models import Provider
from django.db import models
from django.utils import timezone


class Lunch(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    has_veggie = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True, max_length=255)
    date = models.DateField(null=True, default=timezone.now)
    provider = models.ForeignKey(
        Provider, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hr_lunch"
        ordering = ["-date"]
