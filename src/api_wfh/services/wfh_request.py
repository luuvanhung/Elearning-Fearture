import datetime

from api_base.services import BaseService
from api_user.models.user import User
from api_wfh.models.wfh_date import WfhDate
from api_wfh.models.wfh_request import WfhRequest
from api_wfh.serializers.wfh_date import WfhDateSerializer
from api_wfh.serializers.wfh_request import WfhRequestSerializer
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate


class WfhRequestServices(BaseService):
    @classmethod
    def create_wfh_request(cls, data, user):
        request_data = {"reason": data["reason"], "total": data["wfh_total"]}
        wfh_request_serializer = WfhRequestSerializer(data=request_data)
        with transaction.atomic():
            if wfh_request_serializer.is_valid():
                wfh_request = wfh_request_serializer.save(user=user)
            request_id = wfh_request_serializer.data["id"]
            for date in data["date"]:
                date_data = {
                    "date": date["date"],
                    "lunch": date["lunch"],
                    "wfh_request": request_id,
                }
                wfh_date_serializer = WfhDateSerializer(data=date_data)
                if wfh_date_serializer.is_valid():
                    wfh_date_serializer.save(wfh_request=wfh_request)
        return wfh_date_serializer.data

    @classmethod
    def check_valid_wfh_request(cls, data, user: User) -> str:
        error_message = ""
        if cls.is_out_of_join_date(data, user):
            error_message = "There was a request for out of join date!"
        if cls.is_overlap_date(data, user):
            error_message = "There was a request for this date!"

        return error_message

    @classmethod
    def is_overlap_date(cls, data, user_id):
        list_id_request = WfhRequest.objects.filter(user_id=user_id).values_list(
            "id", flat=True
        )
        list_dates = [date.get("date") for date in data.get("date")]
        wfh_date = WfhDate.objects.filter(
            date__in=list_dates, wfh_request_id__in=list_id_request
        )
        return wfh_date.exists()

    @classmethod
    def is_out_of_join_date(cls, data, user):
        if user:
            for date_wfh in data.get("date", []):
                date_time_obj = datetime.datetime.strptime(
                    date_wfh["date"], "%Y-%m-%d"
                ).date()
                if date_time_obj < user.timestamp.date():
                    return True
        return False

    @classmethod
    def get_filter_query(cls, request):
        query_name_or_email = request.query_params.get("name_or_email")
        query_name = request.query_params.get("name")
        query_from_date = request.query_params.get("from_date")
        query_to_date = request.query_params.get("to_date")
        filter_args = dict()
        if query_name:
            filter_args["user__profile__name__icontains"] = Collate(
                Value(query_name.strip()), "utf8mb4_general_ci"
            )
        if query_from_date:
            filter_args["wfh_date__date__range"] = [query_from_date, query_to_date]
        queryset = WfhRequest.objects.filter(**filter_args).order_by("-created_at").distinct()
        if query_name_or_email:
            queryset = queryset.filter(Q(user__profile__name__icontains= Collate(Value(query_name_or_email.strip()), "utf8mb4_general_ci")) | Q(user__email__icontains=query_name_or_email))
        return queryset
