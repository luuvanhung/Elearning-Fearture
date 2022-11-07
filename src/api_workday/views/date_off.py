from api_base.views.base import BaseViewSet
from api_workday.models.date_off import DateOff
from api_workday.serializers.date_off import DateOffSerializer
from common.constants.api_constants import HttpMethod
from common.constants.workday_constants import Workday
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class DateOffViewSet(BaseViewSet):
    queryset = DateOff.objects.all()
    serializer_class = DateOffSerializer
    required_alternate_scopes = {
        "create": [["request_off:edit"]],
        "get_date_off_user_effect": [["request_off:edit"]],
    }

    def create(self, request, *args, **kwargs):
        serializer = DateOffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_date_off_user_effect(self, request, *args, **kwargs):
        unaffected_status = [Workday.STATUS_REJECTED, Workday.STATUS_CANCELED]
        date_offs = DateOff.objects.filter(request_off__profile= request.user.profile)\
            .exclude(request_off__status__in = unaffected_status)
        serializers = self.get_serializer(date_offs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
