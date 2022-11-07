from api_base.views import BaseViewSet
from api_lunch.models import Lunch
from api_lunch.serializers import LunchSerializer
from rest_framework import status
from rest_framework.response import Response


class LunchViewSet(BaseViewSet):
    required_alternate_scopes = {
        "create": [["lunches:edit"]],
        "retrieve": [["lunches:view"]],
        "update": [["lunches:edit"]],
        "destroy": [["lunches:edit"]],
        "list": [["lunches:view"]],
    }
    serializer_class = LunchSerializer
    queryset = Lunch.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LunchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error_msg": str(e)})
