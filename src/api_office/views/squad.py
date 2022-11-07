from api_base.views import BaseViewSet
from api_office.models import Squad
from api_office.serializers import SquadSerializer
from api_office.services import OfficeService
from common.constants.api_constants import HttpMethod
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class SquadViewSet(BaseViewSet):
    queryset = Squad.objects.all()
    serializer_class = SquadSerializer
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "list": [["office:view"]],
        "import_squads": [["office:edit"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        return Response(self.get_queryset().values("id", "name"))

    @action(methods=[HttpMethod.POST], detail=False, url_path="import-squads")
    def import_squads(self, request, *args, **kwargs):
        try:
            OfficeService.import_squads(request.data)
            return Response({"message": "Import squads successfully!"}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
