from datetime import datetime

from core.settings.base import PUBLIC_KEY
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_access_token_model
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import verify_signed_token
from oauthlib.oauth2.rfc6749.utils import scope_to_list


class CustomOAuth2Validator(OAuth2Validator):
    def validate_bearer_token(self, token, scopes, request):
        """
        When users try to access resources, check that provided token is valid
        """
        if not token:
            return False

        introspection_url = oauth2_settings.RESOURCE_SERVER_INTROSPECTION_URL
        introspection_token = oauth2_settings.RESOURCE_SERVER_AUTH_TOKEN
        introspection_credentials = (
            oauth2_settings.RESOURCE_SERVER_INTROSPECTION_CREDENTIALS
        )
        try:
            payload = verify_signed_token(PUBLIC_KEY, token)
            user_id = payload.get("sub", None)
            user = get_user_model().objects.get(pk=user_id) if user_id else None
            unix_timestamp = float(payload.get("exp", None))
            expires = datetime.fromtimestamp(unix_timestamp)
            scope = " ".join(payload.get("scope", None))
            request.user = user
            request.scopes = payload.get("scope", None)
            access_token = get_access_token_model()(
                user=user, token=token, expires=expires, scope=scope
            )
            request.access_token = access_token
            return True

        except Exception:
            # if there is no token or it's invalid then introspect the token if there's an external OAuth server

            if introspection_url and (introspection_token or introspection_credentials):
                access_token = self._get_token_from_authentication_server(
                    token,
                    introspection_url,
                    introspection_token,
                    introspection_credentials,
                )

                if access_token and access_token.is_valid(scopes):
                    request.client = access_token.application
                    request.user = access_token.user
                    request.scopes = scopes

                    # this is needed by django rest framework
                    request.access_token = access_token
                    return True
                return False

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        """
        Ensure required scopes are permitted (as specified in the settings file)
        """
        # special scope for the default client
        all = {"__all__"}
        client_scopes = set(scope_to_list(client.scope))
        if all.issubset(scopes) and all.issubset(client_scopes):
            return True

        available_scopes = set(
            get_scopes_backend().get_available_scopes(
                application=client, request=request
            )
        )
        return set(scopes).issubset(available_scopes)

    def get_additional_claims(self, request):
        # Add more information here
        return {
            "sub": request.user.id,
            "aud": request.client.id,
        }


def get_scopes_backend():
    scopes_class = oauth2_settings.SCOPES_BACKEND_CLASS
    return scopes_class()
