from api_base.views import BaseViewSet
from api_oauth2.models import ApiKey
from api_oauth2.permissions.api_key_permissions import HasOauth2ApiKey
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_oauth2.serializers import ApiKeySerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ApiViewSet(BaseViewSet):
    serializer_class = ApiKeySerializer
    queryset = ApiKey.objects.all()
    permission_classes = [TokenHasActionScope | HasOauth2ApiKey]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        application_id = request.data.get("application_id")
        scope = request.data.get("scope")
        api_key, key = ApiKey.objects.create_key(
            name=name, scope=scope, application_id=application_id
        )
        return Response(key, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["DELETE"], url_path="delete-by-prefix")
    def delete_by_prefix(self, request):
        prefix = request.data.get("prefix")
        if not prefix:
            return Response(
                {"msg": "prefix invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        ApiKey.objects.filter(prefix=prefix).delete()
        return Response({"msg": "delete success"}, status=status.HTTP_200_OK)
