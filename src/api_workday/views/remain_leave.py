import datetime

from api_base.views import BaseViewSet
from api_user.models.profile import Profile
from api_workday import cron_tab
from api_workday.models.remain_leave import RemainLeave
from api_workday.serializers.remain_leave import RemainLeaveSerializer
from api_workday.services.remain_leave import RemainLeaveService
from common.constants.api_constants import HttpMethod
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class RemainLeaveViewSet(BaseViewSet):
    serializer_class = RemainLeaveSerializer
    queryset = RemainLeave.objects
    required_alternate_scopes = {
        "create": [["remain_leave:edit"]],
        "retrieve": [["remain_leave:view"]],
        "update": [["remain_leave:edit"]],
        "destroy": [["remain_leave:edit"]],
        "create_remain_leave": [["remain_leave:edit"]],
        "list": [["remain_leave:view"]],
        "retrieve_date": [["remain_leave:view"]],
        "remain_leave_user": [["remain_leave:view"]],
    }

    def create(self, request, *args, **kwargs):
        next_year = RemainLeaveService.get_next_year()
        if (
                next_year == datetime.datetime.now().year + 1
                and not RemainLeave.objects.filter(year=next_year).exists()
        ):
            with transaction.atomic():
                for profile in Profile.objects.all():
                    RemainLeaveService.create_annual_leave(
                        year=next_year, profile=profile
                    )
                return Response(
                    RemainLeaveService.get_annual_leave_by_year(next_year),
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {"status": "Year has been used"}, status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        year = RemainLeaveService.get_next_year()
        if RemainLeave.objects.filter(year=kwargs.get("year") | year).exists():
            return Response(
                RemainLeaveService.get_annual_leave_by_year(
                    year=kwargs.get("year") | year
                )
            )
        else:
            return Response(
                {"status": "Year has been used"}, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        data = request.data
        remain_leave = RemainLeave.objects.filter(
            profile__id=request.data.get("profile")["id"], year=request.data.get("year")
        ).first()
        if remain_leave is None:
            remain_leave = RemainLeave.objects.filter(pk=request.data.get("id")).first()

        profile = Profile.objects.filter(pk=request.data.get("profile")["id"]).first()
        data["profile"] = profile
        if str(remain_leave.id) == str(request.data.get("id")):
            serializer_remain_leave = self.get_serializer(
                remain_leave, data=data, partial=True
            )
            serializer_remain_leave.is_valid(raise_exception=True)
            self.perform_update(serializer_remain_leave)
            return Response(serializer_remain_leave.data, status=status.HTTP_200_OK)
        return Response(
            {"status": "This year has been exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=[HttpMethod.GET], detail=False)
    def remain_leave_user(self, request, *args, **kwargs):
        user_id = request.query_params.get("id")
        profile = Profile.objects.filter(user__id=user_id).first()
        return Response(RemainLeaveService.get_remain_leave_user(profile), status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=False)
    def create_remain_leave(self, request, *args, **kwargs):
        data = request.data
        profile = Profile.objects.filter(pk=request.data.get("profile")["id"]).first()
        remain_leave = RemainLeave.objects.filter(year=request.data.get("year"))
        if len(remain_leave) > 0:
            return Response(
                {"status": "This year has been exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer_remain_leave = RemainLeaveSerializer(data=data)
        with transaction.atomic():
            if serializer_remain_leave.is_valid():
                serializer_remain_leave.save(profile=profile)
        return Response(serializer_remain_leave.data, status=status.HTTP_201_CREATED)

    @action(methods=[HttpMethod.GET], detail=False)
    def retrieve_date(self, request, *args, **kwargs):
        profile = request.user.profile
        data = RemainLeaveService.retrieve_remain_leaves(profile)
        if data is None:
            return Response(
                {"status": "Office setting not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def add_annual_leave(self, request, *args, **kwargs):
        cron_tab.add_annual_leave()
        return Response({"status": "test add annual leave"}, status=status.HTTP_200_OK)
