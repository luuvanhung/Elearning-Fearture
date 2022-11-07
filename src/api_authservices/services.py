import google.auth.transport.requests
from api_oauth2.services import AuthorizationOauth2
from api_user.services import UserService
from core.settings.base import EMAIL_DOMAIN, LIMIT_DOMAIN
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.response import Response

GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"


class AuthServices:
    @classmethod
    def google_get_user_profile(cls, token: str):
        try:
            request = google.auth.transport.requests.Request()
            id_info = id_token.verify_oauth2_token(token, request)
            if "accounts.google.com" in id_info["iss"]:
                return id_info
        except:
            return False

    @classmethod
    def login_google(cls, id_token):
        user_data = cls.google_get_user_profile(str(id_token))
        if not user_data:
            return Response(
                {"Token": "The token is either invalid or has expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        profile_data = {
            "sub": user_data["sub"],
            "email": user_data["email"],
            "first_name": user_data["given_name"],
            "last_name": user_data["family_name"],
            "iss": user_data["iss"],
        }
        if LIMIT_DOMAIN is False or (
            LIMIT_DOMAIN is True and user_data["email"].split("@")[1] == EMAIL_DOMAIN
        ):
            user, _ = UserService.check_account_linking(**profile_data)
            if user is None:
                return Response(
                    {"Unauthorized": "Our account has not been linked"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            password = id_token
            request_oauth2 = AuthorizationOauth2.authorization_oauth2(
                user.email, password
            )
            data = request_oauth2.json()
            if request_oauth2.status_code == 200:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": "You cannot login with this email"},
            status=status.HTTP_400_BAD_REQUEST,
        )
