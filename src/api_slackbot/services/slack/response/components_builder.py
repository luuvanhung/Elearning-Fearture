import json

from django.conf import settings

from api_elearning.models import Assignment
from api_user.models import Profile
from api_workday.services.leave_type import LeaveTypeService
from common.constants.slack_constants import (
    NotificationDialogContent,
    RequestDialogContent,
    SlackActionId,
    SlackEnumMessages,
    SlackInputTriggerActionType,
)
from common.constants.slack_constants.enum_messages import FormLeaveRequest, NotifyAssignmentForUser
from common.constants.wit_constants.intents import WitIntent
from common.constants.workday_constants.date import Workday
from utils.string_utils import Utils
from .base_components_builder import BaseComponentsBuilder


class ValidRequestResponseBuilder(BaseComponentsBuilder):
    def __init__(self, message_dto, temp_leave_request_id):
        super().__init__()
        self.message_dto = message_dto
        self.temp_leave_request_id = temp_leave_request_id

    def create_title(self):
        if self.message_dto.get("user_intent") == WitIntent.CREATE_LEAVE_REQUEST:
            self.create_header_text(RequestDialogContent.LEAVE_REQUEST_TITLE)
        elif self.message_dto.get("user_intent") == WitIntent.CREATE_WFH_REQUEST:
            self.create_header_text(RequestDialogContent.WFH_REQUEST_TITLE)
        return self

    def create_from_date_section(self):
        self.create_mrkdwn_text("*From:*")
        from_date_elements = [
            self.sub_component_builder.date_picker_builder(
                place_holder="Select starting leave date",
                initial_date=self.message_dto.get("date_time").get("from_date"),
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.SELECT_STARTING_DATE,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
            ),
            self.sub_component_builder.static_select_builder(
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.SELECT_STARTING_TIME,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
                place_holder="Select starting leave time",
                initial_option={
                    "value": self.message_dto.get("date_time").get("from_time"),
                    "text": self.message_dto.get("date_time").get("from_time"),
                },
                selections=[
                    {
                        "value": Workday.DEFAULT_START_HOUR,
                        "text": Workday.DEFAULT_START_HOUR,
                    },
                    {
                        "value": Workday.DEFAULT_START_HOUR_AFTERNOON,
                        "text": Workday.DEFAULT_START_HOUR_AFTERNOON,
                    },
                ],
            ),
        ]
        self.create_actions_section(action_elements=from_date_elements)
        return self

    def create_to_date_section(self):
        self.create_mrkdwn_text("*To:*")
        to_date_elements = [
            self.sub_component_builder.date_picker_builder(
                place_holder="Select end leave date",
                initial_date=self.message_dto.get("date_time").get("to_date"),
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.SELECT_END_DATE,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
            ),
            self.sub_component_builder.static_select_builder(
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.SELECT_END_TIME,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
                place_holder="Select end leave time",
                initial_option={
                    "value": self.message_dto.get("date_time").get("to_time"),
                    "text": self.message_dto.get("date_time").get("to_time"),
                },
                selections=[
                    {
                        "value": Workday.DEFAULT_END_HOUR_MORNING,
                        "text": Workday.DEFAULT_END_HOUR_MORNING,
                    },
                    {
                        "value": Workday.DEFAULT_END_HOUR,
                        "text": Workday.DEFAULT_END_HOUR,
                    },
                ],
            ),
        ]
        self.create_actions_section(action_elements=to_date_elements)
        return self

    def create_reason(self):
        self.interactive_response_dto.append(
            self.sub_component_builder.plain_input_builder(
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.REASON_INPUT,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
                label="Reason (I know your reason only when you press the Enter key after typing it!):",
                place_holder="Why you want to be off on that day?",
                initial_value=self.message_dto.get("reason"),
                trigger_actions_on=SlackInputTriggerActionType.ON_ENTER_PRESS,
            )
        )
        return self

    def create_leave_type(self, leave_types_data, default_leave_type):
        if self.message_dto.get("user_intent") == WitIntent.CREATE_LEAVE_REQUEST:
            leave_type_accessory = self.sub_component_builder.static_select_builder(
                action_id=json.dumps(
                    {
                        "action_type": SlackActionId.SELECTED_LEAVE_TYPE,
                        "temp_leave_request_id": self.temp_leave_request_id,
                    }
                ),
                place_holder=RequestDialogContent.LEAVE_TYPE_PLACEHOLDER,
                selections=[
                    {
                        "value": leave_type.get("id"),
                        "text": leave_type.get("name"),
                    }
                    for leave_type in leave_types_data
                ],
                initial_option={
                    "text": default_leave_type.get("name"),
                    "value": Utils.get_id(default_leave_type.get("id")),
                },
            )

            self.create_accessory_section(
                section_title=RequestDialogContent.LEAVE_TYPE_SECTION_TITLE,
                accessory=leave_type_accessory,
            )
            return self

    def create_remain_leave(self, remain_leaves):
        if self.message_dto.get("user_intent") == WitIntent.CREATE_LEAVE_REQUEST:
            self.create_mrkdwn_text(
                RequestDialogContent.REMAIN_LEAVE_TITLE + " " + str(remain_leaves)
            )
        return self

    def create_take_lunch_option(self, lunch_status=False):
        action_id = json.dumps(
            {
                "action_type": SlackActionId.HAVE_LUNCH_CHECKED,
                "temp_leave_request_id": self.temp_leave_request_id,
            }
        )
        options = [
            {
                "text": RequestDialogContent.TAKE_LUNCH_TITLE,
                "description": RequestDialogContent.TAKE_LUNCH_DESCRIPTION,
                "value": SlackActionId.HAVE_LUNCH_CHECKED,
            }
        ]

        if lunch_status:
            initial_options = options[0]
            self.create_actions_section(
                action_elements=[
                    self.sub_component_builder.checkboxes_builder(
                        action_id=action_id,
                        options=options,
                        initial_option=initial_options,
                    )
                ]
            )

        else:
            self.create_actions_section(
                action_elements=[
                    self.sub_component_builder.checkboxes_builder(
                        action_id=action_id, options=options
                    )
                ]
            )
        return self

    def create_interactive_button(self):
        self.create_actions_section([self.confirm_button(), self.cancel_button()])
        return self

    def create_hrm_link(self):
        if self.message_dto.get("user_intent") == WitIntent.CREATE_LEAVE_REQUEST:
            self.interactive_response_dto.append(
                self.sub_component_builder.section_mrkdwn_text_builder(
                    mrkdwn_text="_<"
                                + settings.HRM_NEW_LEAVE_REQUEST_LINK
                                + "|"
                                + RequestDialogContent.HRM_CREATE_LEAVE_LINK_CONTENT
                                + ">_"
                )
            )
        elif self.message_dto.get("user_intent") == WitIntent.CREATE_WFH_REQUEST:
            self.interactive_response_dto.append(
                self.sub_component_builder.section_mrkdwn_text_builder(
                    mrkdwn_text="_<"
                                + settings.HRM_NEW_WFH_REQUEST_LINK
                                + "|"
                                + RequestDialogContent.HRM_CREATE_WFH_LINK_CONTENT
                                + ">_"
                )
            )
        return self

    def confirm_button(self):
        request_type_for_button_values = Workday.LEAVE
        if self.message_dto.get("user_intent") == WitIntent.CREATE_WFH_REQUEST:
            request_type_for_button_values = Workday.WFH

        return self.create_button(
            button_data={
                "text": RequestDialogContent.CREATE_BUTTON_TEXT,
                "style": "primary",
            },
            button_values={
                "action": "created",
                "type": request_type_for_button_values,
            },
            action_id_data={
                "action_type": SlackActionId.BUTTON_CREATED,
                "temp_leave_request_id": self.temp_leave_request_id,
            },
            confirm_data={
                "title": RequestDialogContent.CONFIRM_CREATE_TITLE,
                "text": RequestDialogContent.CONFIRM_CREATE_TEXT,
                "confirm": RequestDialogContent.CONFIRM_CREATE_ACTION_TEXT,
                "deny": RequestDialogContent.DENY_CREATE_ACTION_TEXT,
            },
        )

    def cancel_button(self):
        return self.create_button(
            button_data={
                "text": RequestDialogContent.CANCEL_BUTTON_TEXT,
                "style": "danger",
            },
            button_values={"action": "canceled"},
            action_id_data={
                "action_type": SlackActionId.BUTTON_CANCELED,
                "temp_leave_request_id": self.temp_leave_request_id,
            },
            confirm_data={
                "title": RequestDialogContent.CONFIRM_CANCEL_TITLE,
                "text": RequestDialogContent.CONFIRM_CANCEL_TEXT,
                "confirm": RequestDialogContent.CONFIRM_CANCEL_ACTION_TEXT,
                "deny": RequestDialogContent.DENY_CANCEL_ACTION_TEXT,
            },
        )


class DuplicateRequestResponseBuilder(BaseComponentsBuilder):
    def __init__(self, temp_leave_request_id):
        super().__init__()
        self.temp_leave_request_id = temp_leave_request_id

    def create_message(self):
        self.create_mrkdwn_text(SlackEnumMessages.DUPLICATE_REQUEST_MESSAGE)
        return self

    def create_interactive_button(self, user_message):
        self.create_actions_section(
            [self.continue_making_button(user_message), self.new_request_button()]
        )
        return self

    def continue_making_button(self, user_message):
        return self.create_button(
            button_data={
                "text": RequestDialogContent.CONTINUE_MAKING_BUTTON_TEXT,
                "style": "primary",
            },
            button_values={
                "action": "continue making",
            },
            action_id_data={
                "action_type": SlackActionId.BUTTON_CONTINUE_MAKING,
                "temp_leave_request_id": self.temp_leave_request_id,
                "user_message": user_message,
            },
        )

    def new_request_button(self):
        return self.create_button(
            button_data={
                "text": RequestDialogContent.CREATE_NEW_BUTTON_TEXT,
                "style": "danger",
            },
            button_values={"action": "new request"},
            action_id_data={
                "action_type": SlackActionId.BUTTON_NEW_REQUEST,
            },
        )


class LeaveRequestNotificationToLineManagerBuilder(BaseComponentsBuilder):
    def __init__(self, profile: Profile, profile_approver: Profile = None):
        super().__init__()
        self.profile = profile,
        self.profile_approver = profile_approver

    def create_title(self, title):
        self.create_header_text(text=title)
        return self

    def create_content(self):
        self.create_mrkdwn_text(
            text=f":wave: Dear *{self.profile_approver.name}*, an employee has created a leave request as detail:"
        )
        return self

    def create_leave_request_detail(
            self, list_dates, leave_type_id, reason, date_quantity
    ):
        request_datetime = self.get_request_datetime(list_dates)
        leave_type_name = LeaveTypeService.get_leave_type_by_id(
            leave_type_id=leave_type_id
        ).name
        leave_request_detail = (
                FormLeaveRequest.NAME
                + self.profile[0].name
                + "* \n"
                + FormLeaveRequest.TEAMS
                + self.profile[0].teams
                + "* \n"
                + FormLeaveRequest.DURATION
                + request_datetime.get("from_datetime")
                + FormLeaveRequest.TO
                + request_datetime.get("to_datetime")
                + "*\n"
                + FormLeaveRequest.QUANTITY
                + date_quantity
                + "*\n"
                + FormLeaveRequest.LEAVE_TYPE
                + leave_type_name
                + "*\n"
                + FormLeaveRequest.REASON
                + reason
                + "*\n"
        )

        self.create_mrkdwn_text(text=leave_request_detail)
        return self

    def create_interactive_button(self, request_off_id, list_dates):
        self.create_actions_section(
            [
                self.approve_button(request_off_id, list_dates),
                self.deny_button(request_off_id, list_dates),
            ]
        )
        return self

    def create_request_off_hrm_link(self):
        self.interactive_response_dto.append(
            self.sub_component_builder.section_mrkdwn_text_builder(
                mrkdwn_text="_<"
                            + settings.HRM_APPROVAL_REQUEST_LINK
                            + "|"
                            + NotificationDialogContent.HRM_APPROVAL_LINK_CONTENT
                            + ">_"
            )
        )
        return self

    def approve_button(self, request_off_id, list_dates):
        return self.create_button(
            button_data={
                "text": NotificationDialogContent.APPROVE_BUTTON_TEXT,
                "style": "primary",
            },
            button_values={
                "action": "approve request",
                "list_dates": list_dates,
            },
            action_id_data={
                "action_type": SlackActionId.BUTTON_APPROVE_REQUEST,
                "request_off_id": request_off_id,
            },
            confirm_data={
                "title": NotificationDialogContent.CONFIRM_APPROVE_TITLE,
                "text": NotificationDialogContent.CONFIRM_APPROVE_TEXT,
                "confirm": NotificationDialogContent.CONFIRM_APPROVE_ACTION_TEXT,
                "deny": NotificationDialogContent.CANCEL_APPROVE_ACTION_TEXT,
            },
        )

    def deny_button(self, request_off_id, list_dates):
        return self.create_button(
            button_data={
                "text": NotificationDialogContent.DENY_BUTTON_TEXT,
                "style": "danger",
            },
            button_values={"action": "deny request", "list_dates": list_dates},
            action_id_data={
                "action_type": SlackActionId.BUTTON_DENY_REQUEST,
                "request_off_id": request_off_id,
            },
            confirm_data={
                "title": NotificationDialogContent.CONFIRM_DENY_TITLE,
                "text": NotificationDialogContent.CONFIRM_DENY_TEXT,
                "confirm": NotificationDialogContent.CONFIRM_DENY_ACTION_TEXT,
                "deny": NotificationDialogContent.CANCEL_DENY_ACTION_TEXT,
            },
        )

    @staticmethod
    def get_request_datetime(list_dates):
        from_date = list_dates[0].get("date")
        from_time = (
            "08:00"
            if list_dates[0].get("type") != Workday.AFTERNOON_SHIFT_TIME
            else "13:30"
        )
        to_date = list_dates[len(list_dates) - 1].get("date")
        to_time = (
            "17:30"
            if list_dates[len(list_dates) - 1].get("type") != Workday.MORNING_SHIFT_TIME
            else "12:00"
        )

        return dict(
            from_datetime=from_date + " " + from_time,
            to_datetime=to_date + " " + to_time,
        )


class LeaveRequestApprovedNotificationToTeamBuilder(BaseComponentsBuilder):
    def __init__(self):
        super().__init__()

    def create_title(self, title):
        self.create_mrkdwn_text(text=title)
        return self

    def create_leave_request_detail(self, date_time, reason):
        leave_request_detail = (
                FormLeaveRequest.DURATION
                + date_time.get("from_datetime")
                + FormLeaveRequest.TO
                + date_time.get("to_datetime")
                + "*\n"
                + FormLeaveRequest.REASON
                + reason
                + "*"
        )
        self.create_mrkdwn_text(text=leave_request_detail)
        return self


class LeaveRequestActionedNotificationToEmployeeBuilder(BaseComponentsBuilder):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile

    def create_title(self, title):
        self.create_header_text(text=title)
        return self

    def create_leave_request_detail(self, date_time, leave_type_name, reason):
        leave_request_detail = (
                FormLeaveRequest.NAME
                + self.profile.name
                + "* \n"
                + FormLeaveRequest.TEAMS
                + self.profile.teams
                + "* \n"
                + FormLeaveRequest.DURATION
                + date_time.get("from_datetime")
                + FormLeaveRequest.TO
                + date_time.get("to_datetime")
                + "*\n"
                + FormLeaveRequest.QUANTITY
                + date_time.get("total")
                + "*\n"
                + FormLeaveRequest.LEAVE_TYPE
                + leave_type_name
                + "*\n"
                + FormLeaveRequest.REASON
                + reason
                + "*\n"
        )
        self.create_mrkdwn_text(text=leave_request_detail)
        return self

    def create_hrm_leave_request_link(self):
        self.interactive_response_dto.append(
            self.sub_component_builder.section_mrkdwn_text_builder(
                mrkdwn_text="_<"
                            + settings.HRM_APPROVAL_REQUEST_LINK
                            + "|"
                            + NotificationDialogContent.HRM_APPROVAL_MEMBER_LINK_CONTENT
                            + ">_"
            )
        )
        return self


class CancelingLeaveRequestResponseBuilder(BaseComponentsBuilder):
    def __init__(self, pending_leave_requests_list):
        super().__init__()
        self.pending_leave_requests_list = pending_leave_requests_list

    def create_title(self):
        self.create_header_text(RequestDialogContent.CANCEL_REQUEST_TITLE)
        return self

    def create_preface_sentence(
            self, preface_sentence=RequestDialogContent.DELETE_REQUEST_PREFACE_SENTENCE
    ):
        self.create_mrkdwn_text(preface_sentence)
        return self

    def create_leave_request_list_for_canceling(self):
        self.interactive_response_dto.append(
            self.sub_component_builder.divider_builder()
        )
        for request_off in self.pending_leave_requests_list:
            request_date_off = request_off.get("date_off")
            from_datetime = request_date_off[len(request_date_off) - 1]
            to_datetime = request_date_off[0]
            from_date = from_datetime.get("date")
            from_time = self.get_from_time_by_date_off_type(from_datetime.get("type"))
            to_date = to_datetime.get("date")
            to_time = self.get_from_time_by_date_off_type(to_datetime.get("type"))
            self.create_accessory_section(
                section_title=self.leave_request_detail_builder(
                    request_off=dict(
                        from_date=from_date,
                        from_time=from_time,
                        to_date=to_date,
                        to_time=to_time,
                        total_dates=request_off.get("total"),
                        leave_type_name=request_off.get("leave_type").get("name"),
                        reason=request_off.get("reason"),
                    )
                ),
                accessory=self.confirm_button(request_off.get("id")),
            )
            self.interactive_response_dto.append(
                self.sub_component_builder.divider_builder()
            )
        return self

    def create_note_sentence(self):
        self.create_mrkdwn_text(RequestDialogContent.SOME_REQUEST_NOT_IN_LIST_NOTE)
        return self

    def create_hrm_link(self):
        self.interactive_response_dto.append(
            self.sub_component_builder.section_mrkdwn_text_builder(
                mrkdwn_text="_<"
                            + settings.HRM_LEAVE_REQUEST_LINK
                            + "|"
                            + RequestDialogContent.HRM_CANCEL_LEAVE_LINK_CONTENT
                            + ">_"
            )
        )
        return self

    def create_cancel_process_button(self):
        self.create_actions_section([self.cancel_button()])
        return self

    def confirm_button(self, request_off_id):
        return self.create_button(
            button_data={
                "text": RequestDialogContent.DELETE_REQUEST_BUTTON_TEXT,
                "style": "primary",
            },
            button_values={
                "action": "delete_request",
            },
            action_id_data={
                "action_type": SlackActionId.BUTTON_DELETE_REQUEST,
                "request_off_id": request_off_id,
            },
            confirm_data={
                "title": RequestDialogContent.CONFIRM_DELETE_TITLE,
                "text": RequestDialogContent.CONFIRM_DELETE_TEXT,
                "confirm": RequestDialogContent.CONFIRM_DELETE_ACTION_TEXT,
                "deny": RequestDialogContent.DENY_DELETE_ACTION_TEXT,
            },
        )

    def cancel_button(self):
        return self.create_button(
            button_data={
                "text": RequestDialogContent.CANCEL_DELETE_REQUEST_BUTTON_TEXT,
                "style": "danger",
            },
            button_values={"action": "canceled"},
            action_id_data={
                "action_type": SlackActionId.BUTTON_CANCEL_DELETE_REQUEST,
            },
            confirm_data={
                "title": RequestDialogContent.CONFIRM_CANCEL_DELETE_REQUEST_TITLE,
                "text": RequestDialogContent.CONFIRM_CANCEL_DELETE_REQUEST_TEXT,
                "confirm": RequestDialogContent.CONFIRM_CANCEL_DELETE_REQUEST_ACTION_TEXT,
                "deny": RequestDialogContent.DENY_CANCEL_DELETE_REQUEST_ACTION_TEXT,
            },
        )

    @staticmethod
    def leave_request_detail_builder(request_off):
        return (
                FormLeaveRequest.DURATION
                + request_off.get("from_date")
                + " "
                + request_off.get("from_time")
                + FormLeaveRequest.TO
                + request_off.get("to_date")
                + " "
                + request_off.get("to_time")
                + "* \n"
                + FormLeaveRequest.QUANTITY
                + str(request_off.get("total_dates"))
                + "* \n"
                + FormLeaveRequest.LEAVE_TYPE
                + request_off.get("leave_type_name")
                + "* \n"
                + FormLeaveRequest.REASON
                + (
                    f"*{request_off.get('reason')}*"
                    if request_off.get("reason") != ""
                    else FormLeaveRequest.NO_DATA
                )
        )


class CanceledRequestResponseBuilder(BaseComponentsBuilder):
    def __init__(self, deleted_request):
        super().__init__()
        self.deleted_request = deleted_request

    def create_title(self):
        self.create_header_text(RequestDialogContent.DELETED_REQUEST_RESPONSE_TITLE)
        return self

    def create_canceled_request_detail(self):
        self.create_mrkdwn_text(
            "Duration: *"
            + self.deleted_request.get("date_off")[-1].get("date")
            + " "
            + self.get_from_time_by_date_off_type(
                self.deleted_request.get("date_off")[-1].get("type")
            )
            + "* to *"
            + self.deleted_request.get("date_off")[0].get("date")
            + " "
            + self.get_from_time_by_date_off_type(
                self.deleted_request.get("date_off")[0].get("type")
            )
            + "* \n"
            + "Quantity: *"
            + str(self.deleted_request.get("total"))
            + "* \n"
            + "Leave type: *"
            + self.deleted_request.get("leave_type").get("name")
            + "* \n"
            + "Reason:"
            + (
                f"*{self.deleted_request.get('reason')}*"
                if self.deleted_request.get("reason") != ""
                else " *_No data_*"
            )
        )
        return self


class CancelLeaveRequestNotification(BaseComponentsBuilder):
    def __init__(self, title):
        super().__init__()
        self.title = title

    def create_title(self):
        self.create_header_text(text=self.title)
        return self

    def create_content(self, requester: Profile, choosed_approver: Profile):
        if self.title == RequestDialogContent.CANCEL_LEAVE_REQUEST_TITLE:
            title_text = f":wave: Dear *{choosed_approver.name}*, an employee has a cancel leave request. Details:"
        elif self.title == RequestDialogContent.APPROVE_CANCEL_LEAVE_REQUEST_TITLE:
            title_text = f":wave: Dear *{requester.name}*, your cancel leave request has been approved. Details:"
        elif self.title == RequestDialogContent.REJECT_CANCEL_LEAVE_REQUEST_TITLE:
            title_text = f":wave: Dear *{requester.name}*, your cancel leave request has been rejected " \
                         f"and your leave request will be approved. Details:"
        self.create_mrkdwn_text(text=title_text)
        return self

    def create_leave_request_detail(
            self, requester: Profile, date_offs: list, name_leave_type: str, reason: str, date_quantity: float
    ):
        request_datetime = self.get_request_datetime(list_dates=date_offs)
        from_datetime = request_datetime.get("from_datetime")
        to_datetime = request_datetime.get("to_datetime")
        request_detail = (
            f"{FormLeaveRequest.NAME}{requester.name}* \n"
            f"{FormLeaveRequest.TEAMS}{requester.teams}* \n"
        )
        if not self.title == RequestDialogContent.CANCEL_LEAVE_REQUEST_TITLE:
            request_detail = ""
        self.create_mrkdwn_text(
            f"{request_detail}"
            f"{FormLeaveRequest.DURATION}{from_datetime}{FormLeaveRequest.TO}{to_datetime}* \n"
            f"{FormLeaveRequest.QUANTITY}{date_quantity}* \n"
            f"{FormLeaveRequest.LEAVE_TYPE}{name_leave_type}* \n"
            f"{FormLeaveRequest.REASON}{reason}* \n"
        )
        return self

    @staticmethod
    def get_request_datetime(list_dates: list):
        from_date = list_dates.first().date
        from_time = (
            "08:00"
            if list_dates.first().date != Workday.AFTERNOON_SHIFT_TIME
            else "13:30"
        )
        to_date = list_dates.last().date
        to_time = (
            "17:30"
            if list_dates.last().type != Workday.MORNING_SHIFT_TIME
            else "12:00"
        )

        return dict(
            from_datetime=f"{from_date} {from_time}",
            to_datetime=f"{to_date} {to_time}",
        )

    def create_hrm_link(self):
        if self.title == RequestDialogContent.CANCEL_LEAVE_REQUEST_TITLE:
            self.interactive_response_dto.append(
                self.sub_component_builder.section_mrkdwn_text_builder(
                    mrkdwn_text=f"_{NotificationDialogContent.HRM_APPROVAL_LINK_CONTENT}"
                                f" | <https://{settings.URL_WEB_INTERNAL}>_"
                )
            )
        else:
            self.interactive_response_dto.append(
                self.sub_component_builder.section_mrkdwn_text_builder(
                    mrkdwn_text=f"_Please check mail for more information!_"
                )
            )
        return self


class SendNotificationAssignment(BaseComponentsBuilder):
    def __init__(self, assignment: Assignment = None):
        super().__init__()
        self.assignment = assignment
        self.profile = assignment.user.profile

    def create_notify_assignment_detail(self):
        leave_request_detail = (
                f"{NotifyAssignmentForUser.NEW_ASSIGNMENT_TITLE}"
                + f":wave: Dear *{self.profile.name}*,\n"
                + f":point_right: You are now being enrolled in *{self.assignment.course_name}*"
        )
        if self.assignment.due_date:
            leave_request_detail += f" . You must complete your training by {self.assignment.due_date}"

        leave_request_detail += (
                f"\n:point_right: The assignments you've been enrolled in are displayed below: *{self.assignment.course_name}*"
                + f"\n:point_right: Please use the link below to start your training: \n   "
                  f"<{self.assignment.link_to_course}>"
        )
        self.create_mrkdwn_text(text=leave_request_detail)
        return self


class SendNotificationAssignmentDaily(BaseComponentsBuilder):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def create_notify_assignment_detail(self):
        message = (f"{NotifyAssignmentForUser.TITLE}"
                   + f"Dear *{self.data['user'].profile.name}*,\n"
                   + f"These following assignments need to be completed:\n")
        for assignment in self.data['assignments']:
            message += f"\n :point_right:*<{assignment['link_to_course']}|{assignment['course_title']}>*"
            if assignment['days_left']:
                message += f" with *{assignment['days_left']}* days left"

        message += "\n\nPlease click on Assignment's title to continue what you are working on!"
        self.create_mrkdwn_text(text=message)
        return self
