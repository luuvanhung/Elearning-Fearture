from api_slackbot.services.slack.response.base_components_builder import (
    SubComponentBuilder,
)
from api_workday.services.leave_type import LeaveTypeService
from api_workday.services.remain_leave import RemainLeaveService
from common.constants.datetime_constant.weekday import WeekDay
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from common.constants.workday_constants.date import Workday
from utils.datetime_utils import (
    date_string_to_datetime,
    extract_duration_to_list_of_dates,
)


class CreatedButtonService:
    @classmethod
    def create_request_data_processing(cls, profile, button_values, temp_leave_request):

        # Handle case: If user select "to_date" smaller than "from_date
        if date_string_to_datetime(
            temp_leave_request.from_date
        ) > date_string_to_datetime(temp_leave_request.to_date):
            return {
                "is_exception": True,
                "response_blocks": [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=SlackEnumMessages.INVALID_END_DATE_MESSAGE
                    )
                ],
            }

        # Get list of requested date
        list_of_requested_dates = extract_duration_to_list_of_dates(
            from_date=temp_leave_request.from_date,
            to_date=temp_leave_request.to_date,
            week_day_remove=[WeekDay.SATURDAY, WeekDay.SUNDAY],
        )

        if len(list_of_requested_dates) <= 0:
            return {
                "is_exception": True,
                "response_blocks": [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=SlackEnumMessages.ONLY_WEEKEND_MESSAGE
                    )
                ],
            }

        if button_values.get("type") == Workday.WFH:
            return cls.mapping_requested_data_to_service(
                leave_request=temp_leave_request,
                dates=list_of_requested_dates,
                reason=temp_leave_request.reason,
                type=button_values.get("type"),
            )

        else:
            remain_leaves = RemainLeaveService.retrieve_remain_leaves(profile)
            leave_type = LeaveTypeService.get_leave_type_by_id(
                temp_leave_request.leave_type_id
            )
            if remain_leaves is not None and cls.is_valid_quantity_requested_days(
                len(list_of_requested_dates),
                leave_type.days,
                remain_leaves.get("current_days_off"),
            ):
                return cls.mapping_requested_data_to_service(
                    leave_request=temp_leave_request,
                    dates=list_of_requested_dates,
                    reason=temp_leave_request.reason,
                    type=button_values.get("type"),
                )

            else:
                return {
                    "is_exception": True,
                    "response_blocks": [
                        SubComponentBuilder().section_mrkdwn_text_builder(
                            mrkdwn_text=SlackEnumMessages.INVALID_QUANTITY_DAYS_MESSAGE
                        )
                    ],
                }

    @classmethod
    def is_valid_quantity_requested_days(
        cls, quantity_requested, limit_days, remain_leave
    ):
        return quantity_requested <= limit_days and quantity_requested <= remain_leave

    @classmethod
    def mapping_requested_data_to_service(cls, leave_request, dates, reason, type):
        mapped_to_service = {"type_id": leave_request.leave_type_id, "reason": reason}

        # Handle case: full day leave request
        if (
            leave_request.from_time == Workday.DEFAULT_START_HOUR
            and leave_request.to_time == Workday.DEFAULT_END_HOUR
        ):
            requested_dates = cls.mapping_requested_date_to_service(
                list_of_dates=dates,
                type_of_leave=Workday.FULL,
                lunch_status=leave_request.lunch_status,
            )
            mapped_to_service["date"] = requested_dates
            if type == Workday.LEAVE:
                mapped_to_service["total_leaves"] = len(requested_dates)
                return mapped_to_service
            if type == Workday.WFH:
                mapped_to_service["wfh_total"] = len(requested_dates)
                return mapped_to_service

        # Handle case: half-day and full-day in one leave request
        # so there will be 1 date is half-day leave and the rest are full-day leaves
        elif len(dates) >= 2:
            # Handle cases: All day is full-day leave except the last one and first one in list(dates)
            if (
                leave_request.from_time == Workday.DEFAULT_START_HOUR_AFTERNOON
                and leave_request.to_time == Workday.DEFAULT_END_HOUR_MORNING
            ):
                mapped_to_service["total_leaves"] = len(dates) - 1

                requested_dates = cls.mapping_requested_date_to_service(
                    list_of_dates=dates[0:1],
                    type_of_leave=Workday.AFTERNOON,
                    lunch_status=leave_request.lunch_status,
                )
                requested_dates.extend(
                    cls.mapping_requested_date_to_service(
                        list_of_dates=dates[1 : len(dates) - 1],
                        type_of_leave=Workday.FULL,
                        lunch_status=False,
                    )
                )
                requested_dates.extend(
                    cls.mapping_requested_date_to_service(
                        list_of_dates=dates[len(dates) - 1 : len(dates)],
                        type_of_leave=Workday.MORNING,
                        lunch_status=leave_request.lunch_status,
                    )
                )
                mapped_to_service["date"] = requested_dates
                return mapped_to_service

            else:
                mapped_to_service["total_leaves"] = len(dates) - 0.5

                # Handle cases: All day is full-day leave except the last one in list(dates)
                """
                    request_datetime:{
                        "from_time": 08:00,
                        "from_date": 22/02/2022,
                        "to_time": 12:00,
                        "from_date": 25/02/2022
                    }
                """
                if (
                    leave_request.from_time == Workday.DEFAULT_START_HOUR
                    and leave_request.to_time == Workday.DEFAULT_END_HOUR_MORNING
                ):
                    requested_dates = cls.mapping_requested_date_to_service(
                        list_of_dates=dates[0 : len(dates) - 1],
                        type_of_leave=Workday.FULL,
                        lunch_status=False,
                    )
                    requested_dates.extend(
                        cls.mapping_requested_date_to_service(
                            list_of_dates=dates[len(dates) - 1 : len(dates)],
                            type_of_leave=Workday.MORNING,
                            lunch_status=leave_request.lunch_status,
                        )
                    )
                    mapped_to_service["date"] = requested_dates
                    return mapped_to_service

                # Handle cases: All day is full-day leave except the first one in list(dates)
                """
                    request_datetime:{
                        "from_time": 13:30,
                        "from_date": 22/02/2022,
                        "to_time": 17:30,
                        "from_date": 25/02/2022
                    }
                """
                if (
                    leave_request.from_time == Workday.DEFAULT_START_HOUR_AFTERNOON
                    and leave_request.to_time == Workday.DEFAULT_END_HOUR
                ):
                    requested_dates = cls.mapping_requested_date_to_service(
                        list_of_dates=dates[0:1],
                        type_of_leave=Workday.AFTERNOON,
                        lunch_status=leave_request.lunch_status,
                    )
                    requested_dates.extend(
                        cls.mapping_requested_date_to_service(
                            list_of_dates=dates[1 : len(dates)],
                            type_of_leave=Workday.FULL,
                            lunch_status=False,
                        )
                    )
                    mapped_to_service["date"] = requested_dates
                    return mapped_to_service

        # Handle case: Half-day leave request
        else:
            if type == Workday.LEAVE:
                mapped_to_service["total_leaves"] = float(len(dates) / 2)
            if type == Workday.WFH:
                mapped_to_service["wfh_total"] = float(len(dates) / 2)
            # Handle case: morning leave request
            if (
                leave_request.from_time == Workday.DEFAULT_START_HOUR
                and leave_request.to_time == Workday.DEFAULT_END_HOUR_MORNING
            ):
                requested_dates = cls.mapping_requested_date_to_service(
                    dates, Workday.MORNING, leave_request.lunch_status
                )
                mapped_to_service["date"] = requested_dates
            # Handle case: afternoon leave request
            if (
                leave_request.from_time == Workday.DEFAULT_START_HOUR_AFTERNOON
                and leave_request.to_time == Workday.DEFAULT_END_HOUR
            ):
                requested_dates = cls.mapping_requested_date_to_service(
                    dates, Workday.AFTERNOON, leave_request.lunch_status
                )
                mapped_to_service["date"] = requested_dates
            return mapped_to_service

    @staticmethod
    def mapping_requested_date_to_service(
        list_of_dates: list, type_of_leave, lunch_status: bool
    ):
        if type_of_leave == Workday.FULL or type_of_leave == Workday.WFH:
            return [
                dict(
                    date=date,
                    type="All day",
                    lunch=lunch_status,
                    offMorning=True,
                    offAfternoon=True,
                )
                for date in list_of_dates
            ]
        if type_of_leave == Workday.MORNING:
            return [
                dict(
                    date=date,
                    type="08:00-12:00",
                    lunch=lunch_status,
                    offMorning=True,
                    offAfternoon=False,
                )
                for date in list_of_dates
            ]
        if type_of_leave == Workday.AFTERNOON:
            return [
                dict(
                    date=date,
                    type="13:30-17:30",
                    lunch=lunch_status,
                    offMorning=False,
                    offAfternoon=True,
                )
                for date in list_of_dates
            ]
