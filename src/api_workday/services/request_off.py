import datetime

from api_base.services import BaseService
from api_office.models import Office
from api_user.models.profile import Profile
from api_workday.models.date_off import DateOff
from api_workday.models.leave_type import LeaveType
from api_workday.models.remain_leave import RemainLeave
from api_workday.models.request_off import RequestOff
from api_workday.serializers.date_off import DateOffSerializer
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.services.action_request import ActionRequestService
from api_workday.services.send_mail import SendMailRequestOff
from api_workday.services.send_notification_slack import SendNotificationSlack
from api_workday.services.statistic import StatisticServices
from common.constants.workday_constants.date import Workday
from django.db import transaction
from django.db.models import Q, Sum, Value
from django.db.models.functions import Collate


class RequestOffServices(BaseService):
    @classmethod
    def create_request_off_with_approver(
        cls, request_data: dict,
        profile: Profile,
        profile_approver: Profile,
        is_sync_leave_request: bool = False
    ):
        (
            request_off_serializer,
            leave_type_id,
            leave_type,
            list_date_obj,
            request_off_data
        ) = cls.pre_create_request_off(request_data)

        if cls.check_out_of_join_date(request_data, profile.id):
            return {"error": "There was a request for out of join date"}
        elif cls.check_overlap_date(list_date_obj, profile.id):
            return {"error": "There was a request for this date!"}

        with transaction.atomic():
            if request_off_serializer.is_valid():
                request_off = cls.save_request_off(request_off_serializer, leave_type, profile)

            cls.save_date_off(list_date_obj, request_off)

            if is_sync_leave_request:
                ActionRequestService.create_action_user(request_off, profile_approver)
                ActionRequestService.action_approve(
                    request_off.id,
                    profile,
                    comment="OK",
                    is_sync_leave_request=is_sync_leave_request
                )
            elif profile.maximum_level_approved == 0:
                ActionRequestService.create_action_user(request_off, profile)
                ActionRequestService.action_approve(
                    request_off.id, profile, comment="OK"
                )
            else:
                ActionRequestService.create_action_user(
                    request_off, profile_approver
                )
                SendMailRequestOff.send_request(
                    leave_type=leave_type,
                    name_admin=profile_approver.name,
                    name_user=request_off.profile.name,
                    list_email=[profile_approver.personal_email],
                    date_off=request_off.date_off.all(),
                )
                SendNotificationSlack.send_notification_request_off(
                    profile=profile,
                    profile_approver=profile_approver,
                    request_off_data=dict(
                        list_dates=list_date_obj,
                        leave_type_id=leave_type_id,
                        reason=request_off_data.get("reason"),
                        date_quantity=str(request_off_data.get("total")),
                        request_off_id=request_off.id,
                    ),
                )
        return request_off_serializer.data

    @classmethod
    def create_request_off(cls, request_data: dict, profile: Profile, is_sync_leave_request: bool = False) -> dict:
        office = StatisticServices.get_office(profile)

        profile_manager = Profile.objects.filter(user=office.manager).first()
        if (
            profile.line_manager is None
            and profile.maximum_level_approved != 0
            and profile_manager is None
        ):
            return {
                "error": "You don't have any line manger, neither the maximum level and office's manager, office manager is also not found!"
            }

        (
            request_off_serializer,
            leave_type_id,
            leave_type,
            list_date_obj,
            request_off_data
        ) = cls.pre_create_request_off(request_data)

        if cls.check_out_of_join_date(request_data, profile.id):
            return {"error": "There was a request for out of join date"}
        elif cls.check_overlap_date(list_date_obj, profile.id):
            return {"error": "There was a request for this date!"}

        with transaction.atomic():
            if request_off_serializer.is_valid():
                request_off = cls.save_request_off(request_off_serializer, leave_type, profile)

            cls.save_date_off(list_date_obj, request_off)

            if is_sync_leave_request:
                ActionRequestService.create_action_user(request_off, profile)
                ActionRequestService.action_approve(
                    request_off.id,
                    profile,
                    comment="OK",
                    is_sync_leave_request=is_sync_leave_request,
                )
            else:
                if profile.line_manager is not None:
                    ActionRequestService.create_action_user(
                        request_off, profile.line_manager
                    )
                    SendMailRequestOff.send_request(
                        leave_type=leave_type,
                        name_admin=profile.line_manager.name,
                        name_user=request_off.profile.name,
                        list_email=[profile.line_manager.user.email],
                        date_off=request_off.date_off.all(),
                    )
                    SendNotificationSlack.send_notification_request_off(
                        profile=profile,
                        profile_approver=profile.line_manager,
                        request_off_data=dict(
                            list_dates=list_date_obj,
                            leave_type_id=leave_type_id,
                            reason=request_off_data.get("reason"),
                            date_quantity=str(request_off_data.get("total")),
                            request_off_id=request_off.id,
                        ),
                    )
                elif profile.maximum_level_approved == 0:
                    ActionRequestService.create_action_user(request_off, profile)
                    ActionRequestService.action_approve(
                        request_off.id, profile, comment="OK"
                    )
                else:
                    ActionRequestService.create_action_user(
                        request_off, profile_manager
                    )
                    SendMailRequestOff.send_request(
                        leave_type=leave_type,
                        name_admin=profile_manager.name,
                        name_user=request_off.profile.name,
                        list_email=[profile_manager.user.email],
                        date_off=request_off.date_off.all(),
                    )
        return request_off_serializer.data

    @classmethod
    def pre_create_request_off(cls, request_data: dict):
        leave_type_id = request_data.get("type_id", "")
        leave_type = LeaveType.objects.filter(id=leave_type_id).first()
        list_date_obj = request_data.get("date", [])

        request_off_data = {
            "reason": request_data.get("reason", ""),
            "total": request_data.get("total_leaves", 0),
        }
        request_off_serializer = RequestOffSerializer(data=request_off_data)
        return request_off_serializer, leave_type_id, leave_type, list_date_obj, request_off_data

    @classmethod
    def save_request_off(cls, request_off_serializer: RequestOffSerializer, leave_type: LeaveType, profile: Profile):
        request_off = request_off_serializer.save(
            leave_type=leave_type, profile=profile
        )
        return request_off

    @classmethod
    def save_date_off(cls, list_date_obj: list, request_off: RequestOff):
        for date in list_date_obj:
            date_off_data = {
                "date": date["date"],
                "type": date["type"],
                "lunch": date["lunch"],
                "request_off": request_off.id,
            }
            date_off_serializer = DateOffSerializer(data=date_off_data)
            if date_off_serializer.is_valid():
                date_off_serializer.save(request_off=request_off)

    @classmethod
    def check_overlap_date(cls, list_date_obj, profile_id):
        status = [Workday.STATUS_REJECTED, Workday.STATUS_CANCELED]
        for date_obj in list_date_obj:
            date_off = (
                DateOff.objects.filter(date=date_obj["date"])
                .filter(request_off__profile_id=profile_id)
                .exclude(request_off__status__in=status)
            )
            if date_off.exists():
                return True
        return False

    @classmethod
    def check_out_of_join_date(cls, data, profile_id):
        profile = Profile.objects.filter(id=profile_id).first()
        if profile:
            for date_off in data["date"]:
                date_time_obj = datetime.datetime.strptime(
                    date_off["date"], "%Y-%m-%d"
                ).date()
                if date_time_obj < profile.join_date:
                    return True
        return False

    @classmethod
    def get_expired_annual_leave_last_year_in_office_settings(cls):
        office = Office.objects.all().first()
        if office:
            return office.expired_annual_leave_last_year
        return 8

    @classmethod
    def get_the_number_of_days_off(cls, list_date_off):
        date_leave = 0.0
        for date_off in list(list_date_off):
            try:
                if date_off["type"] == Workday.FULL:
                    date_leave += 1
                else:
                    date_leave += 0.5
            except Exception:
                if date_off.type == Workday.FULL:
                    date_leave += 1
                else:
                    date_leave += 0.5
        return date_leave

    @classmethod
    def check_date_off_with_remain_leave(
        cls, total_date, profile_id
    ):
        remain = RemainLeave.objects.filter(profile=profile_id).first()
        if remain:
            if total_date > remain.current_days_off:
                return True
        return False

    @classmethod
    def check_available_date_off(cls, data, profile_id):
        status = [Workday.STATUS_PENDING, Workday.STATUS_FORWARDED]
        list_id_request = RequestOff.objects.filter(
            profile_id=profile_id, status__in=status
        )
        list_date_off = DateOff.objects.filter(request_off__in=list_id_request)
        list_date_leave_request = data.get('date', None)

        total_date = cls.get_the_number_of_days_off(
            list_date_off
        ) + cls.get_the_number_of_days_off(list_date_leave_request)

        if cls.check_date_off_with_remain_leave(
            total_date,
            profile_id,
        ):
            return True
        return False

    @classmethod
    def total_off_by_leave_types(cls, profile_id, leave_type_id, year):
        request_offs = {"total_date_off": 0}
        if profile_id and leave_type_id:
            request_offs = RequestOff.objects.filter(
                profile__id=profile_id,
                leave_type__id=leave_type_id,
                status__in=[Workday.STATUS_APPROVED, Workday.STATUS_FORWARDED, Workday.STATUS_PENDING],
                created_at__year=year,
            ).aggregate(total_date_off=Sum("total"))
            if request_offs["total_date_off"] is None:
                request_offs = {"total_date_off": 0}

        return {"total_leaves": request_offs["total_date_off"]}

    @classmethod
    def get_request_off_by_id(cls, request_off_id):
        return RequestOff.objects.filter(pk=request_off_id).first()

    @classmethod
    def get_pending_request_off(cls, profile_id):
        return RequestOff.objects.filter(
            profile_id=profile_id, status=Workday.STATUS_PENDING
        )

    @classmethod
    def get_filter_query(cls, request):
        query_name_or_email = request.query_params.get('name_or_email')
        query_name = request.query_params.get("name")
        query_email = request.query_params.get("email")
        query_from_date = request.query_params.get("from_date")
        query_to_date = request.query_params.get("to_date")
        query_type_leave = request.query_params.get("type_leave")
        query_status = request.query_params.get("status")
        filter_args = dict()
        if query_name:
            filter_args['profile__name__icontains'] = Collate(Value(query_name.strip()), "utf8mb4_general_ci")
        if query_email:
            filter_args['profile__user__email__icontains'] = query_email
        if query_type_leave:
            filter_args['leave_type'] = query_type_leave
        if query_from_date:
            filter_args['date_off__date__range'] = [query_from_date, query_to_date]
        if query_status:
            filter_args['status'] = query_status
        queryset = RequestOff.objects.filter(**filter_args).order_by("-created_at").distinct()
        if query_name_or_email:
            queryset = queryset.filter(Q(profile__name__icontains= Collate(Value(query_name_or_email.strip()), "utf8mb4_general_ci")) | Q(profile__personal_email__icontains=query_name_or_email))
        return queryset
