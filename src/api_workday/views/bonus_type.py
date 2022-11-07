from api_base.views import BaseViewSet
from api_workday.models import BonusType
from api_workday.serializers import BonusTypeSerializer
from api_workday.services import BonusTypeService
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class BonusTypeViewSet(BaseViewSet):
    queryset = BonusType.objects.all()
    serializer_class = BonusTypeSerializer
    required_alternate_scopes = {
        "list": [["bonus_leave:view"], ["bonus_leave:edit"]],
        "destroy": [['bonus_leave:edit']],
        "create_or_update": [['bonus_leave:edit']]
    }

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=[HttpMethod.POST])
    def create_or_update(self, request, *arg, **kwargs):
        try:
            data = request.data
            bonus_type_id = data.pop('id', 0)
            bonus_type, created = BonusType.objects.update_or_create(id=bonus_type_id, defaults=data)
            return Response(self.get_serializer(bonus_type).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"details": "Can't create or update bonus type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_deleted = BonusTypeService.delete(instance)
        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "Cannot deleted this record"}, status=status.HTTP_400_BAD_REQUEST)
