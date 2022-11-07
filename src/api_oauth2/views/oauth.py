import requests
from core.settings.base import (
    API_HOST,
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    OAUTH2_URL,
)
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    url = OAUTH2_URL + "/api/v1/o/token/"
    payload = {
        "grant_type": "password",
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET,
        "username": request.POST.get("username"),
        "password": request.POST.get("password"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": API_HOST}

    r = requests.post(url, data=payload, headers=headers)
    data = r.json()
    if r.status_code == 200:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([])
def refresh_token_view(request):
    url = OAUTH2_URL + "/api/v1/o/token/"
    payload = {
        "grant_type": "refresh_token",
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET,
        "refresh_token": request.POST.get("refresh_token"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": API_HOST}

    r = requests.post(url, data=payload, headers=headers)
    data = r.json()
    if r.status_code == 200:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([])
def logout_view(request):
    url = OAUTH2_URL + "/api/v1/o/revoke_token/"

    # revoke refresh_token first, to make user can not renew access_token
    payload = {
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET,
        "token_type_hint": "refresh_token",
        "token": request.POST.get("refresh_token"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": API_HOST}
    r = requests.post(url, data=payload, headers=headers)
    if r.status_code != 200:
        return Response(
            {"error": "can not revoke refresh_token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # revoke access_token
    payload = {
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET,
        "token_type_hint": "access_token",
        "token": request.POST.get("access_token"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": API_HOST}
    r = requests.post(url, data=payload, headers=headers)
    if r.status_code != 200:
        return Response(
            {"error": "can not revoke access_token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({"message": "logout success!"}, status=status.HTTP_200_OK)
