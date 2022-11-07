import calendar
import datetime

from django.conf import settings
from django.db.models import Q

from api_base.services.slack import SlackResponseService
from api_slackbot.services.slack.response.slack_response_builder import (
    SlackResponseBuilder,
    slack_exception_message_builder,
)
from api_team.models import TeamMembers
from api_team.models.team import Team
from api_user.models.profile import Profile
from api_workday.models import RequestOff
from common.constants.slack_constants import (
    RequestDialogContent,
    SlackBlocksMessage,
    SlackEnumMessages,
    SlackTextMessage,
)
from common.constants.workday_constants.date import Workday


class SendNotificationSlack:
    slack_response_service = SlackResponseService(settings.SLACK_LEAVE_CHANNEL)

    @classmethod
    def send_notification_request_off(cls, profile: Profile, profile_approver: Profile, request_off_data: dict):
        """
        To send notification to approver from user to request off
        @param profile: profile of user who request off
        @param profile_approver: profile of user who approve request off
        @param request_off_data: data of request off
        """
        channel = cls.get_channel(
            profile_approver=profile_approver,
            default_channel=settings.DEV_SLACK_USER_ID,
        )
        try:
            if channel:
                response_message = (
                    SlackResponseBuilder.create_leave_request_notification_approver(
                        profile, profile_approver, request_off_data
                    )
                )
                if response_message.get("is_exception"):
                    slack_text = SlackTextMessage.ERROR_WHEN_SENDING_NEW_LEAVE_REQUEST_NOTIFICATION
                else:
                    slack_text = SlackTextMessage.NEW_LEAVE_REQUEST
                cls.slack_response_service.send_message(
                    text=slack_text,
                    channel=channel,
                    blocks=response_message.get("response_blocks"),
                )
        except Exception as e:
            cls.slack_response_service.send_message(
                text=SlackTextMessage.ERROR_WHEN_SENDING_NEW_LEAVE_REQUEST_NOTIFICATION,
                channel=channel,
                blocks=slack_exception_message_builder(
                    e,
                    error_title=SlackBlocksMessage.ERROR_WHEN_SENDING_TO_APPROVER_NOTIFICATION_NEW_LEAVE_REQUEST
                ),
            )

    @classmethod
    def send_notification_approve_request_off(
            cls, profile: Profile, request_off_data: RequestOff, request_cancel: bool = False
    ):
        """
        To send notification to Team about request off of user
        @param profile: use to find Slack channel
        @param request_off_data: current user who request off
        @param request_cancel: if request cancel, send notification to user
        """
        # This is just for demo purpose in dev, change this channel later in production
        teams = Team.objects.filter(Q(team_leader=profile.user_id) | Q(team__member=profile.user_id)).distinct()
        channels = [team.slack_channel for team in teams] if teams else []

        employee_slack_id = request_off_data.profile.slack_id
        try:
            (
                from_date,
                from_time,
                to_date,
                to_time,
            ) = cls.get_schedule_channel(request_off_data)

            for slack_channel in channels:
                team_channel = cls.get_channel(
                    specific_channel=slack_channel,
                    default_channel=settings.SLACK_LEAVE_CHANNEL,
                )
                response_message_to_team = (
                    SlackResponseBuilder.create_request_approved_notification_to_team(
                        request_off_data, from_date, from_time, to_date, to_time
                    )
                )

                if response_message_to_team.get("is_exception"):
                    slack_text_to_team = (
                        SlackTextMessage.ERROR_WHEN_SENDING_TO_TEAM_NOTIFICATION_NEW_APPROVED_REQUEST
                    )
                else:
                    slack_text_to_team = (
                        SlackTextMessage.SOME_TEAM_MEMBERS_WILL_NOT_GO_TO_THE_OFFICE_TODAY
                    )
                try:
                    cls.slack_response_service.send_message(
                        channel=team_channel,
                        text=slack_text_to_team,
                        blocks=response_message_to_team.get("response_blocks"),
                    )
                except Exception as e:
                    continue

            if not request_cancel:
                response_message_to_employee = (
                    SlackResponseBuilder.create_request_actioned_notification_to_employee(
                        user_profile=request_off_data.profile,
                        title=SlackEnumMessages.YOUR_REQUEST_HAS_BEEN_APPROVED,
                        date_time=dict(
                            from_datetime=f"{from_date} {from_time}",
                            to_datetime=f"{to_date} {to_time}",
                            total=str(request_off_data.total),
                        ),
                        leave_type=request_off_data.leave_type.name,
                        reason=request_off_data.reason,
                    )
                )
                if response_message_to_employee.get("is_exception"):
                    slack_text_to_employee = (
                        SlackTextMessage.ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_APPROVED_REQUEST
                    )
                else:
                    slack_text_to_employee = SlackTextMessage.REQUEST_APPROVED
                cls.slack_response_service.send_message(
                    channel=employee_slack_id,
                    text=slack_text_to_employee,
                    blocks=response_message_to_employee.get("response_blocks"),
                )
        except Exception as e:
            if not request_cancel:
                cls.slack_response_service.send_message(
                    text=SlackTextMessage.ERROR_WHEN_SENDING_NEW_LEAVE_REQUEST_NOTIFICATION,
                    channel=employee_slack_id,
                    blocks=slack_exception_message_builder(
                        e,
                        error_title=SlackTextMessage.ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_APPROVED_REQUEST
                    ),
                )

    @classmethod
    def send_notification_reject_request_off(cls, request_off_data):
        """
        To send notification to User who request off
        @param request_off_data: request off of user
        """
        employee_slack_id = request_off_data.profile.slack_id
        try:
            (
                from_date,
                from_time,
                to_date,
                to_time,
            ) = cls.get_schedule_channel(request_off_data)

            if employee_slack_id:
                response_message_to_employee = SlackResponseBuilder.create_request_actioned_notification_to_employee(
                    user_profile=request_off_data.profile,
                    title=SlackEnumMessages.YOUR_REQUEST_HAS_BEEN_REJECTED,
                    date_time=dict(
                        from_datetime=f"{from_date} {from_time}",
                        to_datetime=f"{to_date} {to_time}",
                        total=str(request_off_data.total),
                    ),
                    leave_type=request_off_data.leave_type.name,
                    reason=request_off_data.reason,
                )
                if response_message_to_employee.get("is_exception"):
                    slack_text_to_employee = (
                        SlackTextMessage.ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_REJECTED_REQUEST
                    )
                else:
                    slack_text_to_employee = SlackTextMessage.REQUEST_REJECTED

                cls.slack_response_service.send_message(
                    channel=employee_slack_id,
                    text=slack_text_to_employee,
                    blocks=response_message_to_employee.get("response_blocks"),
                )
        except Exception as e:
            cls.slack_response_service.send_message(
                text=SlackTextMessage.ERROR_WHEN_SENDING_TO_YOU_NOTIFICATION_REJECTED_LEAVE_REQUEST,
                channel=employee_slack_id,
                blocks=slack_exception_message_builder(
                    e,
                    error_title=SlackTextMessage.ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_REJECTED_REQUEST
                ),
            )

    @classmethod
    def send_notification_about_lunch(cls, number_veggies: int, number_lunches: int):
        """
        Send notification to Lunch manager
        @param number_veggies: number of veggies today
        @param number_lunches: number of lunches today
        """
        try:
            today = datetime.date.today()
            convert_today = f"{calendar.day_name[today.weekday()]}, {today.day}/{today.month}/{today.year}"
            response_msg = f":tada: Today is: {convert_today}\n\t:yum: Number of veggies: {number_veggies}\n\t:yum: Number of lunches: {number_lunches}\n\t:yum: Total: {number_veggies + number_lunches}"
            cls.slack_response_service.send_message(text=response_msg)
        except Exception as e:
            cls.slack_response_service.send_message(
                text=SlackTextMessage.ERROR_WHEN_SENDING_TO_LUNCH_MANAGER_NOTIFICATION,
                blocks=slack_exception_message_builder(
                    e,
                    error_title=SlackBlocksMessage.ERROR_WHEN_SENDING_TO_LUNCH_MANAGER_NOTIFICATION
                ),
            )

    @staticmethod
    def get_channel(
            profile_approver: Profile = None,
            specific_channel: str = None,
            default_channel: str = settings.DEV_LINE_MANAGER_SLACK_USER_ID,
    ):
        if profile_approver is not None:
            return profile_approver.slack_id
        elif specific_channel is not None and specific_channel != "":
            return specific_channel
        else:
            return default_channel

    @classmethod
    def get_schedule_channel(cls, request_off_data: RequestOff):
        from_date = request_off_data.date_off.last().date
        from_time = (
            Workday.DEFAULT_START_HOUR_AFTERNOON
            if request_off_data.date_off.last().type == Workday.AFTERNOON_SHIFT_TIME
            else Workday.DEFAULT_START_HOUR
        )
        to_date = request_off_data.date_off.first().date
        to_time = (
            Workday.DEFAULT_END_HOUR_MORNING
            if request_off_data.date_off.last().type == Workday.MORNING_SHIFT_TIME
            else Workday.DEFAULT_END_HOUR
        )
        return from_date, from_time, to_date, to_time

    @classmethod
    def send_notification_cancel_leave_request(cls, title: str, requester: Profile, choosed_approver: Profile,
                                               request_off: RequestOff, date_offs: list):
        # To send notification about cancel leave request
        team_member = TeamMembers.objects.filter(member_id=requester.user_id).first()
        team = team_member.team if team_member else None
        profile_receiver = choosed_approver
        if title == RequestDialogContent.APPROVE_CANCEL_LEAVE_REQUEST_TITLE or title == RequestDialogContent.REJECT_CANCEL_LEAVE_REQUEST_TITLE:
            profile_receiver = requester
        channel = cls.get_channel(
            profile_approver=profile_receiver,
            specific_channel=None if team is None else team.slack_channel,
            default_channel=settings.SLACK_LEAVE_CHANNEL,
        )
        try:
            response_message_to_team = (
                SlackResponseBuilder.create_cancel_leave_request_notification(
                    title=title,
                    requester=requester,
                    choosed_approver=choosed_approver,
                    request_off=request_off,
                    date_offs=date_offs
                )
            )
            if response_message_to_team.get("is_exception"):
                slack_text = SlackEnumMessages.ERROR_WHEN_SENDING_NOTICE_ABOUT_CANCEL_LEAVE_REQUEST
            else:
                slack_text = title
            cls.slack_response_service.send_message(
                channel=channel,
                text=slack_text,
                blocks=response_message_to_team.get("response_blocks"),
            )
        except Exception as e:
            cls.slack_response_service.send_message(
                text=SlackEnumMessages.ERROR_WHEN_SENDING_NOTICE_ABOUT_CANCEL_LEAVE_REQUEST,
                channel=channel,
                blocks=slack_exception_message_builder(
                    e,
                    error_title=SlackEnumMessages.ERROR_WHEN_SENDING_NOTICE_ABOUT_CANCEL_LEAVE_REQUEST,
                ),
            )
