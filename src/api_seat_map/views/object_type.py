from api_base.views import BaseViewSet
from api_seat_map.models import ObjectType
from api_seat_map.serializers import ObjectTypeSerializer
from common.constants.api_constants import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class ObjectTypeViewSet(BaseViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            ObjectType.objects.order_by("-created_at").all(), many=True
        )
        return Response(serializer.data)
