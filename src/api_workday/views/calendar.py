from api_base.views.base import BaseViewSet
from api_user.models import Profile
from api_workday.services.calendar import CalendarServices
from common.constants.api_constants.http_method import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class CalendarViewSet(BaseViewSet):
    @action(methods=[HttpMethod.GET], detail=False)
    def admin(self, request, *args, **kwargs):
        response = []
        for profile in Profile.objects.all():
            response.extend(CalendarServices.get_lay_days_by_profile(profile))
        return Response(response)

    @action(methods=[HttpMethod.GET], detail=False)
    def user(self, request, *args, **kwargs):
        profile = request.user.profile
        return Response(CalendarServices.get_lay_days_by_profile(profile))

    @action(methods=[HttpMethod.POST], detail=False, url_path="sync_data")
    def sync_leave_request(self, request, *args, **kwargs):
        time_start = request.data.get("time_start")
        time_end = request.data.get("time_end")
        return CalendarServices.sync_leave_requests(time_start, time_end)
