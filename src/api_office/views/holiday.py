import datetime
import re

from api_base.services import GoogleCalendar
from api_base.views import BaseViewSet
from api_office.models import Holiday, Office
from api_office.serializers import HolidaySerializer
from api_office.services import HolidayService
from common.constants.api_constants import HttpMethod
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.key_constructor.bits import (
    ListSqlQueryKeyBit,
    PaginationKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class CustomListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()


class HolidayViewSet(CacheResponseMixin, BaseViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    object_cache_timeout = 1
    list_cache_timeout = 1
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "list": [["office:view"]],
    }

    def list(self, request, pk=None, *args, **kwargs):
        today = datetime.date.today()
        holidays = Holiday.objects.filter(
            Q(start_year__lte=today.year, end_year__gt=today.year, repeat=True)
            | Q(Q(start_date__year=today.year), Q(end_date__year=today.year)),
            office_id=kwargs["parent_lookup_e"],
        )
        page = self.paginate_queryset(holidays)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        holiday_serializer = self.get_serializer(data=request.data)
        if holiday_serializer.is_valid(raise_exception=True):
            holiday_serializer.save()

        return Response(holiday_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        holiday_id = get_object_or_404(Holiday, pk=kwargs.get("pk"))
        data = Holiday.objects.filter(id=holiday_id.id)
        if data:
            HolidayService.delete_event(data)
            data.delete()
        return Response({"Success": True}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.GET], detail=False)
    def sync_data(self, request, pk=None, *args, **kwargs):
        try:
            items = GoogleCalendar.get_all_event()
            office_data = Office.objects.filter(id=kwargs["parent_lookup_e"])
            pattern = re.compile(f"^{office_data[0].name}")
            for item in items:
                if bool(re.match(pattern, item.get("summary"))):
                    existed_data = Holiday.objects.filter(calendar_id=item.get("id"))
                    new_data = {
                        "office": office_data[0].id,
                        "title": item.get("summary").split(":")[1],
                        "descriptions": item.get("descriptions"),
                        "start_date": item.get("start").get("date"),
                        "end_date": item.get("end").get("date"),
                        "repeat": False,
                        "calendar_id": item.get("id"),
                        "count": 0,
                    }
                    if len(existed_data) == 0:
                        holiday_serializer = self.get_serializer(data=new_data)
                        if holiday_serializer.is_valid(raise_exception=True):
                            holiday_serializer.save()

            return Response(status=status.HTTP_201_CREATED)

        except Exception:
            Exception("Failed to delete event")
            return Response(status=status.HTTP_400_BAD_REQUEST)
