import threading
from collections import defaultdict
from typing import List

from api_base.services import GoogleCalendar
from api_team.models import Team
from api_user.models import Profile
from api_user_lunch.models import UserLunch
from api_workday.models.date_off import DateOff
from api_workday.models.remain_leave import RemainLeave
from api_workday.models.request_detail import RequestDetail
from api_workday.models.request_off import RequestOff
from api_workday.serializers.action_request import RequestDetailSerializer
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.services.date_off import DateOffService
from api_workday.services.remain_leave import RemainLeaveService
from api_workday.services.send_mail import SendMailRequestOff
from api_workday.services.send_notification_slack import SendNotificationSlack
from common.constants.slack_constants.dialog_content import RequestDialogContent
from common.constants.workday_constants import Scopes, Workday
from django.db import transaction
from django.db.models import Q, QuerySet, Value
from django.db.models.functions import Collate
from django.utils import timezone
from lunarcalendar import Converter, Solar
from rest_framework.exceptions import APIException
from utils.datetime_utils import get_current_date


class ActionRequestService:
    @classmethod
    def do_multi_action_request(cls, request):
        data = request.data
        user = request.user.profile
        scopes = request.auth.scopes
        request_off_ids = data.get("request_off_ids")
        comment = data.get("comment")
        action = data.get("action")
        threads = []
        for request_off_id in request_off_ids:
            request_off = RequestOff.objects.filter(id=request_off_id).first()
            if request_off and request_off.status in [Workday.STATUS_REJECTED, Workday.STATUS_APPROVED]:
                raise APIException(f"Your leave request has been {request_off.status}!")
            thread = threading.Thread(
                target=cls.do_action_request,
                args=(
                    {"request_off_id": request_off_id, "comment": comment, "action": action},
                    user,
                    scopes,
                ),
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @classmethod
    def do_action_request(cls, request_data: dict, profile: Profile, scopes: dict):
        request_off_id = request_data.get("request_off_id")
        comment = request_data.get("comment")
        action = request_data.get("action")
        if action == Workday.STATUS_APPROVED:
            data = cls.action_approve(request_off_id=request_off_id, profile=profile, comment=comment, scopes=scopes)
            serializer = RequestDetailSerializer(data, many=True)
        elif action == Workday.STATUS_REJECTED:
            data = cls.action_reject(request_off_id=request_off_id, profile=profile, comment=comment, scopes=scopes)
            serializer = RequestDetailSerializer(data)
        elif action == Workday.STATUS_CANCELING:
            data = cls.action_request_cancel(request_off_id=request_off_id, profile=profile, scopes=scopes)
            serializer = RequestOffSerializer(data)
        else:
            raise APIException(f"{action} Failed")
        return serializer.data

    @classmethod
    def create_action_user(cls, request_off: RequestOff, profile: Profile):
        data = {"request_off": request_off.id, "approve": profile.id}
        serializer = RequestDetailSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(request_off_id=request_off.id)

    @classmethod
    def action_approve(
        cls, request_off_id: str, profile: Profile, comment: str, scopes: dict = None, is_sync_leave_request: bool = False, request_cancel: bool = False
    ):
        scopes = scopes if scopes else {}
        requests_detail = RequestDetail.objects.filter(request_off_id=request_off_id)
        (
            request_off,
            request_detail,
            list_email_manage,
            list_date_off,
        ) = cls.get_request_helper(request_off_id, profile, scopes, requests_detail)
        if request_off.status == Workday.STATUS_CANCELED:
            return request_detail
        if request_off.status == Workday.STATUS_CANCELING:
            return cls.action_approve_cancel(request_off_id=request_off_id, profile=profile)
        level = request_off.profile.maximum_level_approved
        with transaction.atomic():
            if request_off.status != Workday.STATUS_CANCELED:
                condition = (
                    len(requests_detail) < level
                    and profile.line_manager is not None
                    and request_off.leave_type.leave_type_group.is_insurance_pay
                    is False
                )
                if condition:
                    request_off.status = Workday.STATUS_FORWARDED
                    request_off.save()
                    cls.create_action_user(request_off, profile.line_manager)
                    email = {
                        "user": [request_off.profile.user.email],
                        "admin": [profile.line_manager.user.email],
                    }
                    SendMailRequestOff.send_forward_request(
                        name_admin=profile.name,
                        name_admin_manage=profile.line_manager.name,
                        name_user=request_off.profile.name,
                        email=email,
                        date_off=request_off.date_off.all(),
                    )
                else:
                    request_off.status = Workday.STATUS_APPROVED
                    if request_off.leave_type.leave_type_group.is_company_pay and request_off.leave_type.is_count:
                        RemainLeaveService.handle_annual_leave(
                            request_off.profile,
                            DateOffService.get_num_days_off(request_off),
                        )
                    request_off.save()
                    cls.change_lunch(list_date_off, request_off)

                    if not is_sync_leave_request:
                        if request_cancel:
                            SendMailRequestOff.send_reject_cancel_request_to_user(
                                leave_type=request_off.leave_type,
                                name_user=request_off.profile.name,
                                name_admin=profile.name,
                                list_email=[request_off.profile.user.email],
                                date_offs=request_off.date_off.all(),
                            )
                            SendMailRequestOff.send_reject_cancel_request_to_manage(
                                leave_type=request_off.leave_type,
                                name_user=request_off.profile.name,
                                name_admin=profile.name,
                                choosed_approver=request_detail.approve.name,
                                list_email=list_email_manage,
                                date_offs=request_off.date_off.all(),
                            )
                        else:
                            SendMailRequestOff.send_approve_request_to_user(
                                leave_type=request_off.leave_type,
                                name_admin=profile.name,
                                name_user=request_off.profile.name,
                                list_email=[request_off.profile.user.email],
                                date_off=request_off.date_off.all(),
                            )
                            SendMailRequestOff.send_approve_request_to_manage(
                                leave_type=request_off.leave_type,
                                name_user=request_off.profile.name,
                                name_admin=profile.name,
                                choosed_approver=request_detail.approve.name,
                                email_user=request_off.profile.user.email,
                                list_email=list_email_manage,
                                date_offs=request_off.date_off.all(),
                            )
            request_detail.status = Workday.STATUS_APPROVED
            request_detail.comment = comment
            request_detail.save()

            try:
                if not is_sync_leave_request:
                    if request_cancel:
                        SendNotificationSlack.send_notification_cancel_leave_request(
                            title=RequestDialogContent.REJECT_CANCEL_LEAVE_REQUEST_TITLE,
                            requester=request_off.profile,
                            choosed_approver=request_detail.approve,
                            request_off=request_off,
                            date_offs=request_off.date_off.all()
                        )
                    team = Team.objects.filter(team_leader__profile=profile).first()
                    SendNotificationSlack.send_notification_approve_request_off(
                        profile=request_off.profile, request_off_data=request_off, request_cancel=request_cancel
                    )
                    GoogleCalendar.create_leave_event(
                        request_off=request_off, user_team=team
                    )
            except Exception as e:
                print(e)
        return request_detail

    @classmethod
    def action_reject(cls, request_off_id: str, profile: Profile, scopes: dict, comment: str):
        (
            request_off,
            request_detail,
            list_email_manage,
            list_date_off,
        ) = cls.get_request_helper(request_off_id, profile, scopes)
        if request_off.status == Workday.STATUS_CANCELED:
            return request_detail
        if request_off.status == Workday.STATUS_CANCELING:
            return cls.action_reject_cancel(request_off_id=request_off_id, profile=profile, scopes=scopes)
        with transaction.atomic():
            request_off.status = Workday.STATUS_REJECTED
            request_off.save()
            request_detail.status = Workday.STATUS_REJECTED
            request_detail.comment = comment
            request_detail.save()
            SendMailRequestOff.send_reject_request(
                leave_type=request_off.leave_type,
                name_user=request_off.profile.name,
                name_admin=profile.name,
                reason=request_detail.comment,
                list_email=[request_off.profile.user.email],
                date_offs=list_date_off
            )
            SendMailRequestOff.send_reject_request_to_manage(
                leave_type=request_off.leave_type,
                name_user=request_off.profile.name,
                name_admin=profile.name,
                choosed_approver=request_detail.approve.name,
                list_email=list_email_manage,
                date_offs=list_date_off
            )

            SendNotificationSlack.send_notification_reject_request_off(
                request_off_data=request_off
            )

        return request_detail

    @classmethod
    def action_approve_cancel(cls, request_off_id: str, profile: Profile) -> List[RequestDetail]:
        if profile.user:
            request_off = RequestOff.objects.filter(id=request_off_id).first()
        else:
            request_off = RequestOff.objects.filter(
                id=request_off_id, profile=profile
            ).first()
            if request_off.status == Workday.STATUS_CANCELED:
                raise APIException("The request was canceled earlier")
        date_offs = request_off.date_off.order_by("date")
        if (
            request_off.status == Workday.STATUS_APPROVED
            and DateOffService.get_num_days_off(request_off) > 0
        ):
            RemainLeaveService.handle_annual_leave(
                request_off.profile, -DateOffService.get_num_days_off(request_off)
            )
        request_off.status = Workday.STATUS_CANCELED
        request_off.save()
        request_details = RequestDetail.objects.filter(request_off_id=request_off_id).select_related("approve__user")
        request_details.update(
            status=Workday.STATUS_CANCELED
        )
        SendMailRequestOff.send_approve_cancel_request_to_user(
            leave_type=request_off.leave_type,
            name_user=request_off.profile.name,
            name_admin=profile.name,
            list_email=[request_off.profile.user.email],
            date_offs=date_offs
        )
        list_email = [request_detail.approve.user.email for request_detail in request_details]
        SendMailRequestOff.send_approve_cancel_request_to_manage(
            leave_type=request_off.leave_type,
            name_user=request_off.profile.name,
            name_admin=profile.name,
            choosed_approver=request_details.first().approve.name,
            list_email=list_email,
            date_offs=date_offs
        )
        SendNotificationSlack.send_notification_cancel_leave_request(
            title=RequestDialogContent.APPROVE_CANCEL_LEAVE_REQUEST_TITLE,
            requester=request_off.profile,
            choosed_approver=request_details.first().approve,
            request_off=request_off,
            date_offs=date_offs
        )
        return request_details

    @classmethod
    def allow_or_not_cancel(cls, date_off, profile):
        if profile.user.is_staff:
            return True
        current_date = timezone.now().astimezone().date()
        if date_off.date >= current_date:
            return True
        return False

    @classmethod
    def count_request(cls, profile):
        request_detail = RequestDetail.objects.filter(approve=profile)
        count = request_detail.filter(
            Q(status=None) & ~Q(request_off__status=Workday.STATUS_CANCELED)
        ).count()
        return count

    @classmethod
    def get_request_helper(cls, request_off_id: str, user: Profile, scopes: dict, requests_detail: QuerySet[RequestDetail] = None):
        request_off = RequestOff.objects.filter(id=request_off_id).first()
        requests_detail = requests_detail or RequestDetail.objects.filter(request_off_id=request_off_id)
        list_email_admin = []
        request_detail = None
        for request in requests_detail:
            list_email_admin.append(request.approve.user.email)
            if Scopes.ADMIN_SPECIAL_SCOPE in scopes and not request_detail:
                request_detail = request
            if not request_detail and request.approve == user:
                request_detail = request
        list_date_off = DateOff.objects.filter(request_off__id=request_off_id)
        return request_off, request_detail, list_email_admin, list_date_off

    @classmethod
    def change_lunch(cls, list_date, request_off):
        for date_off in list_date:
            user_lunch = UserLunch.objects.filter(
                profile_id=request_off.profile.id, date=date_off.date
            )
            if date_off.lunch:
                if not user_lunch.exists():
                    data = {"date": date_off.date}
                    solar = Solar(
                        date_off.date.year, date_off.date.month, date_off.date.day
                    )
                    lunar = Converter.Solar2Lunar(solar)
                    if request_off.profile.veggie and (
                        lunar.day == 15 or lunar.day == 1
                    ):
                        data["has_veggie"] = True
                    UserLunch.objects.create(
                        date=data.get("date"),
                        has_veggie=data.get("has_veggie", False),
                        profile_id=request_off.profile.id,
                    )
            else:
                if user_lunch.exists():
                    user_lunch.delete()

    @classmethod
    def action_request_cancel(cls, request_off_id: str, profile: Profile, scopes: dict) -> RequestOff:
        request_off = RequestOff.objects.filter(id=request_off_id).first()
        if request_off and (request_off.status == Workday.STATUS_APPROVED or request_off.status == Workday.STATUS_REJECTED):
            return request_off
        date_offs = request_off.date_off.order_by("date")
        request_off.status = Workday.STATUS_CANCELING
        request_off.save(update_fields=["status"])
        request_details = RequestDetail.objects.filter(request_off_id=request_off_id).select_related("approve__user")
        request_details.update(
            status=Workday.STATUS_CANCELING
        )
        list_email = [request_detail.approve.user.email for request_detail in request_details]
        SendMailRequestOff.send_cancel_request(
            leave_type=request_off.leave_type,
            name_user=profile.name,
            choosed_approver=request_details.first().approve.name,
            list_email=list_email,
            date_offs=date_offs
        )
        SendNotificationSlack.send_notification_cancel_leave_request(
            title=RequestDialogContent.CANCEL_LEAVE_REQUEST_TITLE,
            requester=request_off.profile,
            choosed_approver=request_details.first().approve,
            request_off=request_off,
            date_offs=date_offs
        )
        return request_off

    @classmethod
    def action_reject_cancel(cls, request_off_id: str, profile: Profile, scopes: dict) -> RequestDetail:
        request_off = RequestOff.objects.filter(id=request_off_id).first()
        request_off.status = Workday.STATUS_PENDING
        request_off.save(update_fields=["status"])
        return cls.action_approve(request_off_id=request_off_id, profile=profile, comment="", request_cancel=True, scopes=scopes)

    @classmethod
    def handle_return_day_off_for_request(cls, request_offs):
        date_off_profiles = defaultdict(float)

        for request_off in request_offs:
            if request_off.status == Workday.STATUS_APPROVED:
                off_day_return = cls.get_total_day_off_future(request_off)
                profile_id = request_off.profile.id
                date_off_profiles[profile_id] += off_day_return

        list_profile_id = date_off_profiles.keys()
        bulk_update_data = RemainLeave.objects.filter(profile__in=list_profile_id)
        for remain_leave in bulk_update_data:
            old_current_days_off = remain_leave.current_days_off
            profile_id = remain_leave.profile_id
            new_current_days_off = old_current_days_off + date_off_profiles[profile_id]
            remain_leave.current_days_off = new_current_days_off
        RemainLeave.objects.bulk_update(bulk_update_data, ["current_days_off"])

    @classmethod
    def get_total_day_off_future(cls, request_off) -> float:
        list_date_off = DateOff.objects.filter(request_off=request_off)
        total_day_off = 0
        for date_off in list_date_off:
            if date_off.date > get_current_date():
                total_day_off += (1 if date_off.type == Workday.FULL else 0.5)
        return total_day_off


class FilterActionRequestServices:
    @classmethod
    def filter_multipart(cls, queryset, year, month, day, status, search):
        if year:
            date_off = DateOff.objects.filter(date__year=year)
            if month:
                date_off = date_off.filter(date__month=month)
                if day:
                    date_off = date_off.filter(date__day=day)
            queryset = queryset.filter(request_off__date_off__in=date_off)
        if status:
            queryset = queryset.filter(request_off__status=status)

        if search:
            queryset = queryset.filter(
                Q(request_off__profile__name__icontains=search)
                | Q(request_off__profile__user__email__icontains=search)
                | Q(request_off__reason__icontains=search)
            )
        queryset = list(set(queryset))
        queryset.sort(reverse=True, key=sort_helper)
        return queryset


class FilterRequestServices:
    @classmethod
    def filter_multipart(
        cls, date_type, queryset, year, month, day, search, status=None
    ):
        if year:
            date = date_type.objects.filter(date__year=year)
            if month:
                date = date.filter(date__month=month)
                if day:
                    date = date.filter(date__day=day)
            queryset = queryset.filter(date__in=date)
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(profile__name__icontains=search)
                | Q(profile__user__email__icontains=search)
                | Q(reason__icontains=search)
            )
        queryset = list(set(queryset))
        queryset.sort(reverse=True, key=sort_helper)
        return queryset

    @classmethod
    def get_filter_query(cls, request):
        profile = request.user.profile
        queryset = RequestDetail.objects.filter(approve=profile).order_by("-created_at")
        query_name_or_email = request.query_params.get('name_or_email')
        query_from_date = request.query_params.get("from_date")
        query_to_date = request.query_params.get("to_date")
        query_type_leave = request.query_params.get("type_leave")
        query_status = request.query_params.get("status")
        filter_args = dict()
        if query_type_leave:
            filter_args['request_off__leave_type'] = query_type_leave
        if query_from_date:
            filter_args['request_off__date_off__date__range'] = [query_from_date, query_to_date]
        if query_status:
            filter_args['request_off__status'] = query_status
        queryset = queryset.filter(**filter_args).order_by("-created_at").distinct()
        if query_name_or_email:
            queryset = queryset.filter(
                Q(request_off__profile__name__icontains= Collate(Value(query_name_or_email.strip()), "utf8mb4_general_ci"))
                | Q(request_off__profile__personal_email__icontains=query_name_or_email))
        return queryset


def sort_helper(data):
    return data.created_at.timestamp()
