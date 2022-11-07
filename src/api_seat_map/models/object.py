from api_base.models import TimeStampedModel
from api_seat_map.models import ObjectType
from api_user.models import User
from django.db import models


class Object(TimeStampedModel):
    offset_x = models.FloatField()
    offset_y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    object_type = models.ForeignKey(
        ObjectType, related_name="location_objects", on_delete=models.CASCADE
    )
    managed_by_user = models.ForeignKey(
        User,
        related_name="managed_objects",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    # prioritized: z-index
    prioritized = models.IntegerField(default=0)

    class Meta:
        db_table = "hr_seat_map_object"
