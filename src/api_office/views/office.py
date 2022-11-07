from api_base.views import BaseViewSet
from api_oauth2.permissions.api_key_permissions import HasOauth2ApiKey
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_office.models import Office
from api_office.serializers import OfficeSerializer
from api_office.services import OfficeService
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class OfficeViewSet(BaseViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = [TokenHasActionScope | HasOauth2ApiKey]
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "list": [["office:view"]],
        "get_office_trees": [["office:view"]],
        "get_whole_organization_tree": [["office:view"]],
        "get_all": [["office:view"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_office_trees(self, request, *args, **kwargs):
        root_group = OfficeService.get_node_group_frist(None).first()
        if not root_group:
            return Response(
                {"details": "Not found root group"}, status=status.HTTP_404_NOT_FOUND
            )
        OfficeService.get_office_trees(root_group)
        return Response(root_group, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_whole_organization_tree(self, request, *args, **kwargs):
        root_group = OfficeService.get_node_group_frist(None).first()
        if not root_group:
            return Response(
                {"details": "Not found root group"}, status=status.HTTP_404_NOT_FOUND
            )
        OfficeService.get_tree_group(root_group)
        return Response(root_group, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        return Response(self.get_queryset().values("id", "name"))
