from api_base.views import BaseViewSet
from api_workday.models.request_detail import RequestDetail
from api_workday.models.request_off import RequestOff
from api_workday.serializers.action_request import RequestDetailSerializer
from api_workday.services.action_request import ActionRequestService, FilterActionRequestServices, FilterRequestServices
from common.constants.api_constants import HttpMethod
from common.constants.workday_constants.date import Workday
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ActionRequestDetailViewSet(BaseViewSet):
    queryset = RequestDetail.objects.all()
    serializer_class = RequestDetailSerializer
    required_alternate_scopes = {
        "destroy_multi_request": [["request_off:delete"]],
        "search_request_detail": [["user:access_personal"]],
        "get_request_detail_by_user": [["user:access_personal"]]
    }

    def create(self, request, *args, **kwargs):
        try:
            ActionRequestService.do_multi_action_request(request)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        name_action = request.data.get('action')
        if name_action == Workday.STATUS_CANCELING:
            name_action = "Cancel"
        return Response({"message": f"{name_action} Successfully"}, status=status.HTTP_200_OK)

    def get_request(self, request):
        profile = request.user.profile
        queryset = self.queryset.filter(approve=profile).order_by("-created_at")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")
        status_request = request.query_params.get("status")
        search = request.query_params.get("search")
        queryset = FilterActionRequestServices.filter_multipart(
            queryset, year, month, day, search, status_request
        )
        return queryset

    @action(methods=[HttpMethod.GET], detail=False)
    def get_request_detail_by_user(self, request, *args, **kwargs):
        profile = request.user.profile
        queryset = self.get_queryset().filter(approve=profile).order_by("-created_at")
        page = self.paginate_queryset(queryset)
        serializer = RequestDetailSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=[HttpMethod.GET], detail=False)
    def count(self, request, *args, **kwargs):
        count = ActionRequestService.count_request(request.user.profile)
        data = {"count": count}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=False, url_path="multi")
    def destroy_multi_request(self, request):
        request_off_ids = request.data.get("request_off_ids")
        if request_off_ids:
            queryset = RequestOff.objects.filter(id__in=request_off_ids)
            request_offs_return_day_off = []
            for request_off in queryset:
                if request_off.leave_type.leave_type_group.is_company_pay and request_off.leave_type.is_count:
                    request_offs_return_day_off.append(request_off)
            with transaction.atomic():
                ActionRequestService.handle_return_day_off_for_request(request_offs_return_day_off)
                queryset.delete()

            return Response({"message": f"{request.data.get('action')} Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"{request.data.get('action')} Failed"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def search_request_detail(self, request, *args, **kwargs):
        queryset = FilterRequestServices.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)
