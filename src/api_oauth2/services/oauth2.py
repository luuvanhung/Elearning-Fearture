import requests
from core.settings.base import (
    API_HOST,
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    OAUTH2_URL,
)


class AuthorizationOauth2:
    @classmethod
    def authorization_oauth2(cls, username, password):
        url = OAUTH2_URL + "/api/v1/o/token/"
        payload = {
            "client_type": "public",
            "grant_type": "password",
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "username": username,
            "password": password,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": API_HOST,
        }

        request_oauth2 = requests.post(url, data=payload, headers=headers)
        return request_oauth2
