from api_base.views import BaseViewSet
from api_providers.models import Provider
from api_providers.serializers import ProviderSerializer
from rest_framework import status
from rest_framework.response import Response


class HandleProvider(BaseViewSet):
    pagination_class = None
    serializer_class = ProviderSerializer
    queryset = Provider.objects

    required_alternate_scopes = {
        "create": [["provider:edit"]],
        "retrieve": [["provider:view"]],
        "update": [["provider:edit"]],
        "destroy": [["provider:edit"]],
        "list": [["provider:view"]],
    }

    def list(self, request, *args, **kwargs):
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
