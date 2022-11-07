from api_oauth2.api_key_manager import ApiKeyManager
from django.db import models

# Create your models here.
from oauth2_provider.models import (
    AbstractAccessToken,
    AbstractApplication,
    AbstractGrant,
    AbstractIDToken,
    AbstractRefreshToken,
)
from oauthlib.oauth2.rfc6749.utils import scope_to_list
from rest_framework_api_key.models import AbstractAPIKey


class AccessToken(AbstractAccessToken):
    """
    Change token fields from char field to text field (fix token too long)
    """

    token = models.TextField(blank=True)

    class Meta(AbstractAccessToken.Meta):
        swappable = "OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL"


class RefreshToken(AbstractRefreshToken):
    """
    Change token fields from char field to text field (fix token too long)
    """

    token = models.TextField(blank=True)

    class Meta(AbstractRefreshToken.Meta):
        swappable = "OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL"
        unique_together = ()


class Application(AbstractApplication):
    scope = models.TextField(blank=True)

    class Meta(AbstractApplication.Meta):
        swappable = "OAUTH2_PROVIDER_APPLICATION_MODEL"


class Grant(AbstractGrant):
    class Meta(AbstractGrant.Meta):
        swappable = "OAUTH2_PROVIDER_GRANT_MODEL"


class IDToken(AbstractIDToken):
    class Meta(AbstractIDToken.Meta):
        swappable = "OAUTH2_PROVIDER_ID_TOKEN_MODEL"


class ApiKey(AbstractAPIKey):
    objects = ApiKeyManager()
    scope = models.TextField(blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def has_scopes(self, scopes: str) -> bool:
        if self.scope == "__all__":
            return True
        else:
            key_scopes = set(scope_to_list(self.scope))
            view_scopes = set(scopes)
            return view_scopes.issubset(key_scopes)
