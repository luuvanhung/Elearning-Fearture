from api_base.views import BaseViewSet
from api_office.models import Group
from api_office.serializers import GroupSerializer
from common.constants.api_constants import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "list": [["office:view"]],
        "get_all": [["office:view"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        return Response(self.get_queryset().values("id", "name"))
