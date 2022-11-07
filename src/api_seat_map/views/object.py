from api_base.views import BaseViewSet
from api_seat_map.models import Object
from api_seat_map.serializers import ObjectSerializer
from common.constants.api_constants import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class ObjectViewSet(BaseViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            Object.objects.order_by("-prioritized").all(), many=True
        )
        return Response(serializer.data)
