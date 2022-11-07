import datetime
import threading
from difflib import SequenceMatcher

import unidecode
from api_base.services import BaseService, GoogleCalendar
from api_user.models import Profile
from api_workday.models import LeaveType, RequestOff
from api_workday.models.date_off import DateOff
from api_workday.serializers import DateOffForCalendarSerializer
from api_workday.services.request_off import RequestOffServices
from common.constants.workday_constants import Leave, Workday
from dateutil import parser
from rest_framework import status
from rest_framework.response import Response


class CalendarServices(BaseService):
    @classmethod
    def get_lay_days_by_profile(cls, profile):
        days_off = DateOff.objects.filter(
            request_off__status=Workday.STATUS_APPROVED, request_off__profile=profile
        )
        list_dates = DateOffForCalendarSerializer(days_off, many=True).data
        data = [
            {
                "id": date_off.get("id"),
                "date": date_off.get("date"),
                "type": date_off.get("type"),
                "request_off": date_off.get("request_off"),
                "name": profile.name,
                "email": profile.user.email,
                "lunch": date_off.get("lunch"),
            }
            for date_off in list_dates
        ]
        return data

    @classmethod
    def sync_leave_requests(cls, time_start, time_end):
        if not time_start or not time_end:
            return Response(
                {"error": "time is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        profiles = Profile.objects.all()
        leave_type_default = LeaveType.objects.filter(
            name=Leave.DEFAULT_LEAVE_TYPE
        ).first()
        try:
            calendars = GoogleCalendar.get_all_event(time_start, time_end)
            data_sync_requests_leave = []
            time_end_sync = parser.parse(time_end).strftime("%Y-%m-%d")
            time_start_sync = parser.parse(time_start).strftime("%Y-%m-%d")
            list_requests_off = (
                RequestOff.objects.prefetch_related("date_off")
                .select_related("profile")
                .filter(date_off__date__range=(time_start_sync, time_end_sync))
                .values(
                    "id",
                    "profile",
                    "profile__name",
                    "date_off__date",
                    "request_detail__status",
                    "request_detail__approve_id__user__leader__team_name",
                    "reason",
                    "date_off__type",
                )
            )
            for calendar in calendars:
                request_off = {}
                if calendar.get("creator").get("email").endswith("gserviceaccount.com"):
                    employee_name = calendar.get("summary").split("-")[0].strip()
                else:
                    employee_name = calendar.get("creator").get("email")
                profile = cls.get_id_by_name(profiles, employee_name)
                if profile:
                    leave_type = calendar.get("summary").split("-")[-1].strip()
                    if not cls.check_keyword_in_text(
                        leave_type, ["wfh", "work from home"]
                    ):
                        time_start = calendar.get("start").get("dateTime")
                        time_start = datetime.datetime.strptime(
                            "".join(time_start.rsplit(":", 1)), "%Y-%m-%dT%H:%M:%S%z"
                        )
                        time_end = calendar.get("end").get("dateTime")
                        time_end = datetime.datetime.strptime(
                            "".join(time_end.rsplit(":", 1)), "%Y-%m-%dT%H:%M:%S%z"
                        )
                        duration = time_end.hour - time_start.hour
                        date_off = []
                        if duration > Workday.HALF_DAY_TIME:
                            total_date = 1
                            type_work_day = Workday.FULL
                            off_morning = True
                            off_afternoon = True
                        else:
                            total_date = 0.5
                            if time_start.hour > Workday.END_HOUR_MORNING:
                                type_work_day = Workday.AFTERNOON
                                off_morning = False
                                off_afternoon = True
                            else:
                                type_work_day = Workday.MORNING
                                off_morning = True
                                off_afternoon = False

                        date_off.append(
                            {
                                "date": time_start.strftime("%Y-%m-%d"),
                                "type": type_work_day,
                                "lunch": False,
                                "offMorning": off_morning,
                                "offAfternoon": off_afternoon,
                            }
                        )
                        request_off.update({"date": date_off})
                        request_off.update({"total_leaves": total_date})
                        request_off.update(
                            {"reason": calendar.get("description").split(":")[-1]}
                        )
                        request_off.update({"type_id": str(leave_type_default.id)})
                        data_sync_requests_leave.append(
                            {"profile": profile, "request_off": request_off}
                        )
                else:
                    # Don't get profile by name
                    # Do something
                    pass
            for data_sync_request_leave in data_sync_requests_leave:
                threading.Thread(
                    target=RequestOffServices.create_request_off,
                    args=(
                        data_sync_request_leave.get("request_off"),
                        data_sync_request_leave.get("profile"),
                        True,
                    ),
                ).start()
            for request_off in list_requests_off:
                if (
                    cls.equal_request_off(request_off, data_sync_requests_leave)
                    and request_off.get("request_detail__status") == "Approved"
                ):
                    threading.Thread(
                        target=GoogleCalendar.sync_leave_event,
                        args=(
                            request_off.get("reason"),
                            request_off.get("profile__name"),
                            request_off.get("date_off__type"),
                            request_off.get(
                                "request_detail__approve_id__user__leader__team_name"
                            ),
                            request_off.get("date_off__date"),
                        ),
                    ).start()
            return Response({"data": "sync success"})
        except Exception as e:
            print(e)
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def equal_request_off(cls, request_off, data_sync_requests_leave):
        for data_sync_request_leave in data_sync_requests_leave:
            if data_sync_request_leave.get("request_off").get("date")[0].get(
                "date"
            ) == request_off.get("date_off__date").strftime(
                "%Y-%m-%d"
            ) and data_sync_request_leave.get(
                "profile"
            ).id == request_off.get(
                "profile"
            ):
                return False
        return True

    @classmethod
    def get_id_by_name(cls, profiles, name):
        swapped_first_and_last_name = " ".join(
            name.split(" ")[1:] + [name.split(" ")[0]]
        )
        profile_ratio = {"profile": None, "ratio": -1}
        for profile in profiles:
            similar_profile_ratio = cls.similar(
                profile,
                [
                    cls.remove_accent(name),
                    cls.remove_accent(swapped_first_and_last_name),
                ],
            )
            ratio = similar_profile_ratio.get("ratio")
            if ratio > Workday.RATIO_ACCEPT and ratio > profile_ratio.get("ratio"):
                profile_ratio.update({"profile": profile, "ratio": ratio})
        return profile_ratio.get("profile") if profile_ratio.get("ratio") > -1 else None

    @classmethod
    def check_keyword_in_text(cls, text, keys):
        text = text.lower()
        return any(key in text for key in keys)

    @classmethod
    def remove_accent(cls, text):
        return unidecode.unidecode(text)

    @classmethod
    def similar(cls, profile, names):
        list_of_ratios = [
            {
                "profile_id": profile,
                "ratio": SequenceMatcher(None, profile.name, name).ratio(),
            }
            for name in names
        ]
        return max(list_of_ratios, key=lambda x: x["ratio"])
