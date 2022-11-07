from calendar import monthrange
from datetime import date, datetime
from typing import List

from api_base.services import BaseService
from api_office.models import Department, Holiday, Office
from api_team.models import Team
from api_user.models.profile import Profile
from api_workday.models import LeaveType
from api_workday.models.date_off import DateOff
from api_workday.serializers.date_off import DateOffSerializer
from api_workday.serializers.profile_detail import ProfileDetailSerizlizer
from common.constants.workday_constants import Workday
from django.db.models import Q


class StatisticServices(BaseService):
    @classmethod
    def get_office(cls, profile: Profile):
        if profile.office:
            return profile.office
        else:
            team = Team.objects.filter(team__member=profile.user.id).first()
            if team.office:
                return team.office
            else:
                department = Department.objects.filter(pk=team.department_id).first()
                office = (
                    department.office
                    if department.office is not None
                    else Office.objects.all().first()
                )
                return office

    @classmethod
    def get_holidays(cls, start_date: date, end_date: date, office: Office):
        total = 0
        if start_date and end_date:
            holidays = Holiday.objects.filter(
                office=office, start_date__lte=end_date, end_date__gte=start_date
            ).values_list("start_date", "end_date")
            for holiday in holidays:
                start = max(start_date, holiday[0])
                end = min(end_date, holiday[1])
                total += (int((end - start).days)) + 1
        else:
            holidays = Holiday.objects.filter(office=office).values_list("start_date", "end_date")
            for holiday in holidays:
                total += (int((holiday[1] - holiday[0]).days)) + 1
        return total

    @classmethod
    def get_the_number_of_days_off(cls, list_date_off):
        date_leave = 0
        for date_off in list_date_off:
            if date_off.get("type") == Workday.FULL:
                date_leave += 1
            else:
                date_leave += 0.5
        return date_leave

    @classmethod
    def get_dynamic_type_for_statistic(cls, month, date_off_full):
        data = {}
        leave_types = LeaveType.objects.all().values_list("name", flat=True)
        if not leave_types.exists():
            return data
        date_offs = date_off_full.filter(date__month=month) if month else date_off_full
        serializer_date = DateOffSerializer(date_offs, many=True)
        list_date_off = [
            {
                "date": date.get("date"),
                "type": date.get("type"),
                "lunch": date.get("lunch"),
                "leave_type_name": date.get("request_off").get("type_name"),
            }
            for date in serializer_date.data
        ]
        for leave_type in leave_types:
            detail = []
            for detail_date_off in list_date_off:
                if detail_date_off.get("leave_type_name") == leave_type:
                    detail.append(detail_date_off)
            data[leave_type] = detail
        return data

    @classmethod
    def get_date_off_for_statistic_user_dynamic(cls, year, profile):
        data = []
        try:
            year = int(year)
        except Exception:
            return data
        if year not in range(profile.join_date.year, datetime.now().year + 1):
            return data
        start_month = Workday.FIRST_MONTH + 1
        if year == profile.join_date.year:
            start_month = profile.join_date.month
        date_off_full_in_year = DateOff.objects.filter(
            request_off__status=Workday.STATUS_APPROVED,
            request_off__profile=profile,
            date__year=year,
        )
        leave_types = LeaveType.objects.all().values_list("name", flat=True)
        if not leave_types.exists():
            return data
        for month in range(start_month, Workday.LAST_MONTH + 1):
            details = cls.get_dynamic_type_for_statistic(month, date_off_full_in_year)
            if month and year:
                start_date = datetime(year, month, 1)
                end_date = datetime(year, month, monthrange(year, month)[1])
            profile_date = {
                "profile_id": profile.id,
                "month": month,
                "holidays": cls.get_holidays(
                    start_date=start_date, end_date=end_date, office=profile.office
                ),
                "join_date": profile.join_date,
            }
            for leave_type in leave_types:
                profile_date[leave_type] = details[leave_type]
                profile_date[f"number_{leave_type}"] = cls.get_the_number_of_days_off(
                    details[leave_type]
                )
            data.append(profile_date)
        return data

    @classmethod
    def get_date_off_for_statistic_admin_dynamic(cls, profiles: List[Profile], filters: dict) -> List[dict]:
        leave_types = filters.getlist("leave_types[]")
        search = filters.get("search")
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        data = []
        if search:
            profiles = profiles.filter(Q(name__icontains=search) | Q(user__email__icontains=search))
        if start_date and start_date.year > datetime.now().date().year:
            return data
        if not leave_types:
            leave_types = LeaveType.objects.all().values_list("name", flat=True)
        for profile in profiles:
            if not end_date or end_date >= profile.join_date:
                if start_date and start_date < profile.join_date:
                    start_date = profile.join_date
                filters = {
                    "request_off__status": Workday.STATUS_APPROVED,
                    "request_off__profile": profile
                }
                if start_date and end_date:
                    filters.update({"date__range": (start_date, end_date)})
                date_off_full = DateOff.objects.filter(**filters)
                details = cls.get_dynamic_type_for_statistic(
                    month=None, date_off_full=date_off_full
                )
                serializer_profile = ProfileDetailSerizlizer(profile)
                profile_date = {
                    "id": profile.id,
                    "name": profile.name,
                    "email": serializer_profile.data.get("user").get("email"),
                    "holidays": cls.get_holidays(
                        start_date=start_date, end_date=end_date, office=profile.office
                    ),
                }
                for leave_type in leave_types:
                    profile_date[leave_type] = details[leave_type]
                    profile_date[
                        f"number_{leave_type}"
                    ] = cls.get_the_number_of_days_off(list_date_off=details[leave_type])
                data.append(profile_date)
        return data

    @classmethod
    def get_total_date_off_year_by_team(cls, year, profiles):
        data = []
        try:
            year = int(year)
        except Exception:
            return data
        for profile in profiles:
            profile_data = cls.get_date_off_for_statistic_user_dynamic(
                year=year, profile=profile
            )
            data.append(profile_data)
        return data
