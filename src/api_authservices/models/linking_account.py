import uuid

from api_user.models import User
from django.db import models


class AuthenticationProvider(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    service_name = models.TextField()

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = "hr_authentication_provider"


class LinkingAccount(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        User, related_name="linking_account", on_delete=models.CASCADE
    )
    service_provider = models.ForeignKey(
        AuthenticationProvider, related_name="linking_account", on_delete=models.CASCADE
    )
    account_id = models.TextField()

    def __str__(self):
        return self.account_id

    class Meta:
        db_table = "hr_linking_account"
