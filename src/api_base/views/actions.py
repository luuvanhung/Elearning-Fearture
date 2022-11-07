from api_base.services import LoginService, TokenUtil
from common.constants.api_constants import HttpMethod
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class ActionViewSet(viewsets.ViewSet):
    http_method_names = [HttpMethod.POST, HttpMethod.PUT]
    permission_classes = []

    @action(methods=[HttpMethod.POST], detail=False, url_path="forgot-password")
    def forgot_password(self, request, *args, **kwargs):
        base_link = request.build_absolute_uri("/resetPassword")
        email = request.data.get("email")
        success = LoginService.forgot_password(email, base_link)
        if success:
            return Response({"success": True})
        raise ValidationError("User does not exists")

    @action(methods=[HttpMethod.PUT], detail=False, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        try:
            user = TokenUtil.decode(request.data.get("token"), 1)
        except Exception as e:
            print("Can not decode token", e)
            return Response(
                {"msg": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            password = request.data.get("password")
            LoginService.change_password(user, password)
            return Response({"msg": "success"})
        return Response({"msg": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
