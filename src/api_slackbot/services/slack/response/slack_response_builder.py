from api_elearning.models import Assignment
from api_slackbot.services.exception.exception_message_builder import slack_exception_message_builder
from api_user.models import Profile
from api_workday.models import RequestOff
from api_workday.services.leave_type import LeaveTypeService
from common.constants.datetime_constant.weekday import WeekDay
from common.constants.slack_constants.dialog_content import RequestDialogContent
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from common.constants.wit_constants import WitIntent
from common.constants.workday_constants.date import Workday
from utils.datetime_utils import extract_duration_to_list_of_dates
from utils.string_utils import Utils

from .base_components_builder import SubComponentBuilder
from .components_builder import (
    CanceledRequestResponseBuilder,
    CancelingLeaveRequestResponseBuilder,
    CancelLeaveRequestNotification,
    DuplicateRequestResponseBuilder,
    LeaveRequestActionedNotificationToEmployeeBuilder,
    LeaveRequestApprovedNotificationToTeamBuilder,
    LeaveRequestNotificationToLineManagerBuilder,
    SendNotificationAssignment,
    SendNotificationAssignmentDaily,
    ValidRequestResponseBuilder,
)


class SlackResponseBuilder:
    @classmethod
    def create_valid_request_response(
            cls,
            transferred_intents,
            remain_leaves,
            temp_leave_request_id,
            default_leave_type,
    ):
        try:
            # Collect all leave types from DB
            leave_types_collector = cls.collect_leave_types(
                LeaveTypeService.get_all_leave_type()
            )

            list_of_request_dates = extract_duration_to_list_of_dates(
                from_date=transferred_intents.get("date_time").get("from_date"),
                to_date=transferred_intents.get("date_time").get("to_date"),
                week_day_remove=[WeekDay.SATURDAY, WeekDay.SUNDAY],
            )

            # Handling case: user want to create leave request with saturday and sunday only
            if len(list_of_request_dates) <= 0:
                return {
                    "is_exception": True,
                    "response_blocks": [
                        SubComponentBuilder().section_mrkdwn_text_builder(
                            mrkdwn_text=SlackEnumMessages.ONLY_WEEKEND_MESSAGE
                        )
                    ],
                }

            # Handling case: user want to create half-day leave with multiple days
            elif (
                    transferred_intents.get("date_time").get("type")
                    in [Workday.AFTERNOON, Workday.MORNING]
                    and len(list_of_request_dates) >= 2
            ):
                return {
                    "is_exception": True,
                    "response_blocks": [
                        SubComponentBuilder().section_mrkdwn_text_builder(
                            mrkdwn_text=SlackEnumMessages.ONE_FOR_HALF_DAY_ONLY_MESSAGE
                        )
                    ],
                }

            else:
                # Mapping data from transferred object to Slack response format
                if (
                        transferred_intents.get("user_intent")
                        != WitIntent.CREATE_WFH_REQUEST
                ):
                    slack_response_dto = (
                        ValidRequestResponseBuilder(
                            message_dto=transferred_intents,
                            temp_leave_request_id=Utils.get_id(temp_leave_request_id),
                        )
                        .create_title()
                        .create_from_date_section()
                        .create_to_date_section()
                        .create_reason()
                        .create_leave_type(
                            leave_types_data=leave_types_collector,
                            default_leave_type=default_leave_type,
                        )
                        .create_remain_leave(remain_leaves=remain_leaves)
                        .create_take_lunch_option()
                        .create_interactive_button()
                        .create_hrm_link()
                        .get_response_dto()
                    )
                else:
                    slack_response_dto = (
                        ValidRequestResponseBuilder(
                            message_dto=transferred_intents,
                            temp_leave_request_id=Utils.get_id(temp_leave_request_id),
                        )
                        .create_title()
                        .create_from_date_section()
                        .create_to_date_section()
                        .create_reason()
                        .create_take_lunch_option()
                        .create_interactive_button()
                        .create_hrm_link()
                        .get_response_dto()
                    )
                return {
                    "is_exception": False,
                    "request_date_data": {
                        "from_date": transferred_intents.get("date_time").get(
                            "from_date"
                        ),
                        "from_time": transferred_intents.get("date_time").get(
                            "from_time"
                        ),
                        "to_date": transferred_intents.get("date_time").get("to_date"),
                        "to_time": transferred_intents.get("date_time").get("to_time"),
                    },
                    "response_blocks": slack_response_dto,
                }

        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_duplicate_request_response(cls, temp_leave_request_id, user_message):
        try:
            slack_response_dto = (
                DuplicateRequestResponseBuilder(
                    temp_leave_request_id=Utils.get_id(temp_leave_request_id)
                )
                .create_message()
                .create_interactive_button(user_message)
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_line_manager_actioned_response(
            cls,
            profile,
            title,
            list_dates,
            leave_type_id,
            request_off_reason,
            request_off_total,
    ):
        try:
            slack_response_dto = (
                LeaveRequestNotificationToLineManagerBuilder(profile)
                .create_title(title=title)
                .create_leave_request_detail(
                    list_dates=list_dates,
                    leave_type_id=Utils.get_id(leave_type_id),
                    reason=request_off_reason,
                    date_quantity=str(request_off_total),
                )
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_leave_request_notification_approver(cls, profile: Profile, profile_approver: Profile,
                                                   request_off_data: dict):
        try:
            slack_response_dto = (
                LeaveRequestNotificationToLineManagerBuilder(profile, profile_approver)
                .create_title(title=RequestDialogContent.NEW_LEAVE_REQUEST_TITLE)
                .create_content()
                .create_leave_request_detail(
                    list_dates=request_off_data.get("list_dates"),
                    leave_type_id=Utils.get_id(request_off_data.get("leave_type_id")),
                    reason=request_off_data.get("reason"),
                    date_quantity=request_off_data.get("date_quantity"),
                )
                .create_interactive_button(
                    request_off_id=Utils.get_id(request_off_data.get("request_off_id")),
                    list_dates=request_off_data.get("list_dates"),
                )
                .create_request_off_hrm_link()
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_request_approved_notification_to_team(
            cls, user_request, from_date, from_time, to_date, to_time
    ):
        try:
            slack_response_dto = (
                LeaveRequestApprovedNotificationToTeamBuilder()
                .create_title(
                    f":nhanmetrai: Hi everyone, *{user_request.profile.name}* will be absent as detail:"
                )
                .create_leave_request_detail(
                    date_time=dict(
                        from_datetime=f"{from_date} {from_time}",
                        to_datetime=f"{to_date} {to_time}",
                    ),
                    reason=user_request.reason,
                )
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_request_actioned_notification_to_employee(
            cls, user_profile, title, date_time, leave_type, reason
    ):
        try:
            slack_response_dto = (
                LeaveRequestActionedNotificationToEmployeeBuilder(user_profile)
                .create_title(title)
                .create_leave_request_detail(date_time, leave_type, reason)
                .create_hrm_leave_request_link()
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_canceling_leave_request_response(cls, pending_leave_requests_list):
        try:
            if pending_leave_requests_list:
                slack_response_dto = (
                    CancelingLeaveRequestResponseBuilder(pending_leave_requests_list)
                    .create_title()
                    .create_preface_sentence()
                    .create_leave_request_list_for_canceling()
                    .create_note_sentence()
                    .create_hrm_link()
                    .create_cancel_process_button()
                    .get_response_dto()
                )
                return {
                    "is_exception": False,
                    "response_blocks": slack_response_dto,
                }
            else:
                slack_response_dto = (
                    CancelingLeaveRequestResponseBuilder(pending_leave_requests_list)
                    .create_preface_sentence(
                        preface_sentence=RequestDialogContent.NO_PENDING_REQUEST_AVAILABLE
                    )
                    .create_hrm_link()
                    .get_response_dto()
                )
                return {
                    "is_exception": False,
                    "response_blocks": slack_response_dto,
                }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_canceled_request_response(cls, deleted_request):
        try:
            slack_response_dto = (
                CanceledRequestResponseBuilder(deleted_request)
                .create_title()
                .create_canceled_request_detail()
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def collect_leave_types(cls, leave_types_data):
        res = [
            dict(
                id=Utils.get_id(leave_type.get("id")),
                name=leave_type.get("name"),
                name_type=leave_type.get("name_type"),
            )
            for leave_type in leave_types_data
        ]
        return res

    @classmethod
    def create_cancel_leave_request_notification(cls, title: str, requester: Profile, choosed_approver: Profile,
                                                 request_off: RequestOff, date_offs: list):
        try:
            slack_response_dto = (
                CancelLeaveRequestNotification(title=title)
                .create_title()
                .create_content(requester=requester, choosed_approver=choosed_approver)
                .create_leave_request_detail(
                    requester=requester,
                    date_offs=date_offs,
                    name_leave_type=request_off.leave_type.name,
                    reason=request_off.reason,
                    date_quantity=request_off.total,
                )
                .create_hrm_link()
                .get_response_dto()
            )
            return {
                "is_exception": False,
                "response_blocks": slack_response_dto,
            }
        except Exception as e:
            exception_blocks = slack_exception_message_builder(e)
            return {
                "is_exception": True,
                "response_blocks": exception_blocks,
            }

    @classmethod
    def create_notification_assignment(cls, assignment: Assignment):
        slack_response_dto = SendNotificationAssignment(
            assignment=assignment).create_notify_assignment_detail().get_response_dto()
        return {
            "response_blocks": slack_response_dto,
        }

    @classmethod
    def send_assignments_reminder(cls, data):
        return SendNotificationAssignmentDaily(data).create_notify_assignment_detail().get_response_dto()
