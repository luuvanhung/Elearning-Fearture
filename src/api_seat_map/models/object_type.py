import os
import time

from api_base.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.db import models


def name_file(instance, filename):
    return "seat-map/" + str(round(time.time() * 1000)) + filename


def validate_svg_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == ".svg":
        raise ValidationError("Unsupported file extension.")


class ObjectType(TimeStampedModel):
    name = models.CharField(max_length=50)
    svg_file = models.FileField(
        upload_to=name_file, validators=[validate_svg_extension]
    )

    class Meta:
        db_table = "hr_seat_map_object_type"
