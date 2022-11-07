from api_base.models import BaseOffice
from api_user.models import User
from django.db import models


class Group(BaseOffice):
    manager = models.ForeignKey(
        User, related_name="group", on_delete=models.SET_NULL, null=True, blank=True
    )
    parent_group = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "hr_groups"
