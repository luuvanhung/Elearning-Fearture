import datetime
from typing import List

from api_base.services import BaseService
from api_user.models.profile import Profile
from api_workday.models.date_off import DateOff
from api_workday.models.remain_leave import RemainLeave
from api_workday.serializers.remain_leave import ProfileSerializer, RemainLeaveSerializer
from api_workday.services.date_off import DateOffService
from api_workday.services.statistic import StatisticServices
from common.constants.workday_constants import Leave, Workday
from dateutil.relativedelta import relativedelta
from rest_framework import serializers


class RemainLeaveService(BaseService):
    @classmethod
    def add_annual_leave(cls):
        remain_leaves = RemainLeave.objects.select_related('profile')
        list_update = []
        for remain_leave in remain_leaves:
            if remain_leave.year != datetime.datetime.now().year:
                remain_leave.year = datetime.datetime.now().year
                list_update.append(remain_leave)

            month = remain_leave.profile.join_date.month + Workday.HALF_YEAR
            month = month - Workday.MONTHS_OF_YEAR if month > Workday.MONTHS_OF_YEAR else month

            if month == datetime.datetime.now().month:
                bonus_leave_this_year = remain_leave.profile.total_bonus
                day_off = bonus_leave_this_year + remain_leave.annual_leave + remain_leave.annual_leave_last_year - remain_leave.current_days_off
                day_off = (
                            day_off - remain_leave.annual_leave_last_year) if day_off > remain_leave.annual_leave_last_year else 0
                remain_leave.current_days_off = bonus_leave_this_year + remain_leave.annual_leave - day_off
                list_update.append(remain_leave)
                continue

            if remain_leave.profile.join_date.month == datetime.datetime.now().month:
                remain_leave.annual_leave = cls.get_annual_leave(datetime.datetime.now(), remain_leave.profile.join_date)
                remain_leave.annual_leave_last_year = remain_leave.current_days_off
                remain_leave.current_days_off = remain_leave.annual_leave + remain_leave.annual_leave_last_year
                list_update.append(remain_leave)

        RemainLeave.objects.bulk_update(list_update,
                                        fields=['year', 'annual_leave', 'annual_leave_last_year', 'current_days_off'])

    @classmethod
    def create_annual_leave(cls, **kwargs):
        profile = kwargs.get("profile")
        current_date = kwargs.get("current_date")
        annual_leave = cls.get_annual_leave(current_date, profile.join_date)
        current_dates_off = kwargs.get("remain_leave")
        current_dates_off = float(current_dates_off) if \
            float(current_dates_off) >= 0 else Workday.DEFAULT_ANNUAL_DAY
        annual_leave_last_year = current_dates_off - annual_leave
        data = {
            "annual_leave": annual_leave,
            "current_days_off": current_dates_off,
            "annual_leave_last_year": annual_leave_last_year if annual_leave_last_year > 0 else 0,
            "year": current_date.year
        }
        serializer = RemainLeaveSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save(profile=profile)
        return data

    @classmethod
    def get_annual_leave_by_year(cls, year):
        annual_leaves = RemainLeave.objects.filter(year=year)
        serializer = RemainLeaveSerializer(annual_leaves, many=True)
        return serializer.data

    @classmethod
    def handle_annual_leave(cls, profile, day_leave):
        remain_leave = RemainLeave.objects.get_remain_leave_by_profile_id(id=profile.id)
        if remain_leave.current_days_off < day_leave:
            raise serializers.ValidationError(
                {"status": Workday.STT_NUM_NOT_ENOUGH}
            )
        remain_leave.current_days_off -= day_leave
        remain_leave.save()
        return RemainLeaveSerializer(remain_leave)

    @classmethod
    def get_annual_leave(cls, current_date, join_date):
        default_annual_leave = Workday.DEFAULT_ANNUAL_DAY
        annual_leave_other_year = default_annual_leave + (current_date.year - join_date.year) - (
            1 if current_date.month < join_date.month else 0)
        annual_leave = default_annual_leave if current_date.year == join_date.year else annual_leave_other_year
        return Workday.MAX_ANNUAL_LEAVE if annual_leave > Workday.MAX_ANNUAL_LEAVE else annual_leave

    @classmethod
    def get_next_year(cls):
        list_year = RemainLeave.objects.values_list("year", flat=True)
        if len(list_year) == 0:
            return datetime.datetime.now().year
        return max(list_year) + 1

    @classmethod
    def get_unconfirmed_days(cls, profile: Profile):
        office_setting = StatisticServices.get_office(profile)

        if office_setting is None:
            return Exception("Office setting not found")

        list_date_unconfirmed = DateOff.objects.select_related('request_off').filter(
                request_off__status__in=[Workday.STATUS_FORWARDED, Workday.STATUS_PENDING, Workday.STATUS_CANCELING],
                request_off__profile=profile,
                request_off__leave_type__leave_type_group__is_company_pay=True,
                request_off__leave_type__is_count=Leave.COUNT_DAYS_LEFT)

        unconfirmed_days = (
            DateOffService.get_num_days_off_by_list_date(
                list_date_unconfirmed
            )
        )
        return unconfirmed_days

    @classmethod
    def retrieve_remain_leaves(cls, profile):
        remain_leave = RemainLeave.objects.get_remain_leave_by_profile_id(id=profile.id)
        serializer_remain_leave = RemainLeaveSerializer(remain_leave)
        days_off = RemainLeaveService.get_unconfirmed_days(
            profile
        )
        current_days_off = (
                serializer_remain_leave.data.get("current_days_off") - days_off
        )
        month = profile.join_date.month + Workday.HALF_YEAR
        month = month - Workday.MONTHS_OF_YEAR if month > Workday.MONTHS_OF_YEAR else month
        return {
            "annual_leave": serializer_remain_leave.data.get("annual_leave"),
            "current_days_off": current_days_off,
            "annual_leave_last_year": serializer_remain_leave.data.get("annual_leave_last_year"),
            "profile": serializer_remain_leave.data.get("profile"),
            "month": month,
        }

    @classmethod
    def update_remain_leave_by_profile(cls, profile, old_join_date):
        remain_leave = RemainLeave.objects.filter(profile=profile).first()
        current_date = datetime.datetime.now()
        old_annual_leave = cls.get_annual_leave(current_date=current_date,
                                                join_date=old_join_date)
        new_annual_leave = cls.get_annual_leave(current_date=current_date,
                                                join_date=profile.join_date)
        remain_leave.annual_leave = new_annual_leave

        remain_leave.current_days_off = remain_leave.current_days_off + (new_annual_leave - old_annual_leave)
        return remain_leave.save()

    @classmethod
    def check_expired_annual_leave_last_year(cls, profile):
        current_date = datetime.datetime.now()
        annual_year = current_date.year - profile.join_date.year
        month = current_date.month - profile.join_date.month
        ex_month = month
        if month < 0 and annual_year > 0:
            ex_month = Workday.MONTHS_OF_YEAR + month
            annual_year -= 1
        return ex_month + (Workday.MONTHS_OF_YEAR if annual_year > 0 else 0) > Workday.EXPIRED_MONTH

    @classmethod
    def get_start_date_check_in_year(cls, profile):
        current_date = datetime.datetime.now()
        annual_year = current_date.year - profile.join_date.year
        should_add_year = RemainLeaveService.check_expired_annual_leave_last_year(profile) or annual_year == 0
        start_year = current_date.year + (0 if should_add_year else -1)
        start_year = start_year - (1 if profile.join_date.month > Workday.HALF_YEAR and annual_year > 1 else 0)
        start_date = datetime.date(start_year,
                                   profile.join_date.month,
                                   profile.join_date.day)
        return start_date

    @classmethod
    def get_remain_leave_user(cls, profile):
        current_date = datetime.datetime.now()
        remain_leave = RemainLeave.objects.filter(profile=profile, year=current_date.year).first()
        data = dict()
        data['remain_last_year'] = cls.get_remain_last_year(remain_leave)
        data['bonus_leave_details'] = cls.get_bonus_details(remain_leave)
        data['leave_current_year'] = cls.get_leave_current_year(remain_leave)
        data['profile'] = ProfileSerializer(profile).data
        return data

    @classmethod
    def get_remain_last_year(cls, remain_leave):
        remain_last_year = remain_leave.annual_leave_last_year
        [used_days_remain, used_days_annual_of_last_year] = cls.get_used_days_remain_last_year(remain_leave)
        return {
            "remain_last_year": remain_last_year,
            "used_day_off": used_days_remain,
            "allowed_day_off": remain_last_year - used_days_remain
                                if not cls.check_expired_annual_leave_last_year(remain_leave.profile) else 0,
            "is_expired": cls.check_expired_annual_leave_last_year(remain_leave.profile)
        }

    @classmethod
    def get_bonus_details(cls, remain_leave):
        total_bonus = remain_leave.profile.total_bonus
        used_days = cls.get_used_bonus_year(remain_leave)
        return {
            "total_bonus": total_bonus,
            "used_day_off": used_days,
            "allowed_day_off": total_bonus - used_days
        }

    @classmethod
    def get_leave_current_year(cls, remain_leave):
        [used_days_remain, used_days_annual_of_last_year] = cls.get_used_days_remain_last_year(remain_leave)
        used_day_off = cls.get_used_days_year(remain_leave) \
                       - (used_days_remain + cls.get_used_bonus_year(remain_leave))
        allowed_day_off_last_year = remain_leave.annual_leave_last_year - used_days_remain
        allowed_bonus = remain_leave.profile.total_bonus - cls.get_used_bonus_year(remain_leave)
        return {
            "annual_leave": Workday.DEFAULT_ANNUAL_DAY,
            "seniority_year": remain_leave.annual_leave - Workday.DEFAULT_ANNUAL_DAY,
            "used_day_off": used_day_off,
            "allowed_day_off": remain_leave.current_days_off - (allowed_day_off_last_year + allowed_bonus),
        }

    @classmethod
    def get_used_days_year(cls, remain_leave):
        start_date = cls.get_start_date_check_in_year(remain_leave.profile)
        current_date = datetime.datetime.now()
        date_offs = DateOff.objects.filter(request_off__created_at__date__range=[start_date, current_date],
                                           request_off__profile=remain_leave.profile,
                                           request_off__status=Workday.STATUS_APPROVED)
        date_offs = filter(lambda
                               date_off: date_off.request_off.leave_type.leave_type_group.is_company_pay and date_off.request_off.leave_type.is_count,
                           date_offs)
        return DateOffService.get_num_days_off_by_list_date(date_offs)

    @classmethod
    def get_used_days_remain_last_year(cls, remain_leave) -> List[int]:
        start_date = cls.get_start_date_check_in_year(remain_leave.profile)
        end_date = start_date + relativedelta(months=Workday.HALF_YEAR)
        date_offs = DateOff.objects.filter(request_off__created_at__date__range=[start_date, end_date],
                                           request_off__profile=remain_leave.profile,
                                           request_off__status=Workday.STATUS_APPROVED)
        date_offs = filter(lambda
                               date_off: date_off.request_off.leave_type.leave_type_group.is_company_pay and date_off.request_off.leave_type.is_count,
                           date_offs)
        used_days_remain = DateOffService.get_num_days_off_by_list_date(date_offs)
        used_days_annual = used_days_remain - remain_leave.annual_leave_last_year if used_days_remain > remain_leave.annual_leave_last_year else 0
        used_days_remain = used_days_remain - used_days_annual
        return [used_days_remain, used_days_annual]

    @classmethod
    def get_used_bonus_year(cls, remain_leave) -> int:
        total_bonus = remain_leave.profile.total_bonus
        [used_days_remain, used_days_annual_of_last_year] = cls.get_used_days_remain_last_year(remain_leave)
        used_days = cls.get_used_days_year(remain_leave) - (used_days_remain + used_days_annual_of_last_year)
        total_bonus = total_bonus - used_days_annual_of_last_year
        used_days_bonus = used_days_annual_of_last_year + (used_days if used_days < total_bonus else total_bonus)
        if used_days_annual_of_last_year > total_bonus:
            used_days_bonus = total_bonus
        return used_days_bonus

    @classmethod
    def sync_remain_leave(cls):
        current_date = datetime.datetime.now()
        remain_leaves = RemainLeave.objects.filter(year=current_date.year)
        for remain_leave in remain_leaves:
            used_days_year = cls.get_used_days_year(remain_leave)
            total_bonus = remain_leave.profile.total_bonus
            annual_leave = cls.get_annual_leave(current_date, remain_leave.profile.join_date)
            remain_leave.annual_leave = annual_leave
            remain_leave.current_days_off = remain_leave.annual_leave_last_year + annual_leave + total_bonus - used_days_year
        RemainLeave.objects.bulk_update(remain_leaves,
                                        fields=['annual_leave', 'current_days_off'])
