from api_base.views.base import BaseViewSet
from api_user.models import User
from api_wfh.services.calendar import CalendarServices
from common.constants.api_constants.http_method import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class CalendarViewSet(BaseViewSet):
    @action(methods=[HttpMethod.GET], detail=False)
    def admin(self, request, *args, **kwargs):
        response = []
        for user in User.objects.all():
            response.extend(CalendarServices.get_days_wfh(user))
        return Response(response)

    @action(methods=[HttpMethod.GET], detail=False)
    def user(self, request, *args, **kwargs):
        profile = request.user.profile
        return Response(CalendarServices.get_days_wfh(profile))
