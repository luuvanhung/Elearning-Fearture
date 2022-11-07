from api_authservices.services import AuthServices
from django.contrib.auth import get_user_model
from oauth2_provider.backends import OAuth2Backend
from oauth2_provider.oauth2_backends import get_oauthlib_core

UserModel = get_user_model()
OAuthLibCore = get_oauthlib_core()


# Todo: Handle login for external authentication providers
# Reference: https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#authentication-backends
class CustomOAuth2Backend(OAuth2Backend):
    """
    Authenticate against an OAuth2 access token
    """

    def authenticate(self, request=None, **credentials):
        # For Third party authentication provider
        # Redo this, because it can be call from out side of api server
        try:
            user_data = AuthServices.google_get_user_profile(
                str(credentials["password"])
            )
            if user_data:
                user = UserModel.objects.filter(email=user_data["email"]).first()
                if user is not None:
                    return user
        except Exception as e:
            if request is not None:
                valid, r = OAuthLibCore.verify_request(request, scopes=[])
                if valid:
                    return r.user

        return None
