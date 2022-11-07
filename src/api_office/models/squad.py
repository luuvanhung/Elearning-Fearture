from api_base.models import BaseOffice
from api_office.models import Office
from api_user.models import User
from django.db import models


class Squad(BaseOffice):
    manager = models.ForeignKey(
        User,
        related_name="squad",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    office = models.ForeignKey(
        Office,
        related_name="squad",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "hr_squads"
