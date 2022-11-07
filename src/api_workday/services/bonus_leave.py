import datetime
from typing import List

from api_base.services import BaseService
from api_workday.models import BonusLeave, RemainLeave
from api_workday.serializers import BonusLeaveSerializer
from api_workday.services import RemainLeaveService
from common.constants.workday_constants import Workday
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate


class BonusLeaveService(BaseService):
    @classmethod
    def get_filter_query(cls, request):
        reason = request.query_params.get("reason")
        name = request.query_params.get("name")
        bonus_type_id = request.query_params.get("bonus_type_id")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        filter_args = dict()

        if reason:
            filter_args.update(reason__icontains=reason)
        if bonus_type_id:
            filter_args.update(bonus_type_id=bonus_type_id)
        if from_date:
            filter_args.update(created_at__date__range=[from_date, to_date])
        if name:
            name = Collate(Value(name.strip()), "utf8mb4_general_ci")

        queryset = BonusLeave.objects.filter(Q(profile__name__icontains=name)
                                             | Q(profile__user__email__icontains=name), **filter_args)
        return queryset

    @classmethod
    def add_bonus_days_current_days_off(cls, profile_ids, bonus_days):
        remain_leaves = RemainLeave.objects.filter(profile_id__in=profile_ids)

        for remain_leave in remain_leaves:
            remain_leave.current_days_off += bonus_days
        RemainLeave.objects.bulk_update(remain_leaves, ['current_days_off'])

    @classmethod
    def update_current_day_off(cls, profile, old_bonus_days, new_bonus_days):
        remain_leave = RemainLeave.objects.filter(profile=profile).first()
        remain_leave.current_days_off += (new_bonus_days - old_bonus_days)
        if remain_leave.current_days_off > 0:
            remain_leave.save()
            return True
        return False

    @classmethod
    def bonus_leave_user_year(cls, profile):
        current_date = datetime.datetime.now()
        bonus_leaves = BonusLeave.objects.filter(profile=profile, expired_at__date__gte=current_date)
        serializers = BonusLeaveSerializer(bonus_leaves, many=True)
        return serializers.data

    @classmethod
    def destroy_multi_bonus(cls, bonus_leave_ids: List[str]) -> bool:
        try:
            with transaction.atomic():
                bonus_leaves = BonusLeave.objects.filter(id__in=bonus_leave_ids)
                for bonus_leave in bonus_leaves:
                    destroy_leave = -bonus_leave.bonus_days
                    BonusLeaveService.add_bonus_days_current_days_off([bonus_leave.profile.id], destroy_leave)
                bonus_leaves.delete()
            return True
        except Exception as e:
            return False

    @classmethod
    def add_expired_date_bonus_leave(cls, profile, bonus_leave_id):
        bonus_leave = BonusLeave.objects.filter(id = bonus_leave_id).first()
        valid_from = RemainLeaveService.get_start_date_check_in_year(profile)
        bonus_leave.expired_at = valid_from + relativedelta(months=Workday.EXPIRED_MONTH)
        bonus_leave.save()
