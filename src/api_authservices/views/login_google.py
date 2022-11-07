from api_authservices.services import AuthServices
from rest_framework.views import APIView


class GoogleLoginApi(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        id_token = request.data.get("token")
        return AuthServices.login_google(id_token)
