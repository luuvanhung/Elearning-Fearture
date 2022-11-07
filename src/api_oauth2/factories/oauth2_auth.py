import datetime

from api_oauth2.models import AccessToken, Application
from api_user.models import User
from rest_framework.test import APIClient


class OauthClient(APIClient):
    def authenticate(self, user: User, application: Application):
        app, created = Application.objects.update_or_create(
            defaults={"name": application.name},
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            redirect_uris="https://www.none.com/oauth2/callback",
            name=application.name,
            user=user,
        )
        # Create or update the token, and set it in a default request header.
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        access_token, created = AccessToken.objects.get_or_create(
            defaults={"user": user, "application": app},
            user=user,
            expires=now + datetime.timedelta(seconds=300),
            application=app,
        )
        return access_token.token
