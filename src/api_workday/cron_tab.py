import datetime

from api_base.services import SlackResponseService
from api_slackbot.services.slack.response import SubComponentBuilder
from api_user.models import Profile
from api_workday.models.date_off import DateOff
from api_workday.models.leave_type import LeaveType
from api_workday.services.remain_leave import RemainLeaveService
from common.constants.workday_constants import Workday
from django.conf import settings
from slack_sdk.errors import SlackApiError


def create_remain_leave_for_next_year():
    next_year = RemainLeaveService.get_next_year()
    if next_year == datetime.datetime.now().year + 1:
        for profile in Profile.objects.all():
            RemainLeaveService.create_annual_leave(year=next_year, profile=profile)


def add_annual_leave():
    RemainLeaveService.add_annual_leave()


def get_leave_today():
    today = datetime.date.today()
    date_instance = datetime.date(today.year, today.month, today.day).strftime(
        "%Y-%m-%d"
    )
    channel = settings.SLACK_LEAVE_CHANNEL
    date_offs = DateOff.objects.filter(
        date=date_instance, request_off__status=Workday.STATUS_APPROVED
    )
    if date_offs:
        leave_types = LeaveType.objects.all()

        notice_message = [
            SubComponentBuilder().section_mrkdwn_text_builder(
                ":wave: Hi everyone, let's see who is not going to the office today:"
            )
        ]

        for leave_type in leave_types:
            date_offs_by_type = list(
                filter(
                    lambda date_off: date_off.request_off.leave_type == leave_type,
                    date_offs,
                )
            )
            if date_offs_by_type:
                notice_message.append(
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        content_notice(date_offs_by_type, leave_type.name)
                    )
                )
    else:
        notice_message = [
            SubComponentBuilder().section_mrkdwn_text_builder(
                ":wave: Gud morning to my all dearests, everyone will be in office today :partying_face:"
            )
        ]
    try:
        SlackResponseService(channel=channel).send_message(
            text=(
                "Someone don't go to office today, check it out!"
                if date_offs
                else "No one absent today!"
            ),
            blocks=notice_message,
        )
        return
    except SlackApiError as e:
        raise Exception(e)


def content_notice(date_offs, type_name):
    list_name = [
        date_off.request_off.profile.name + f" ({date_off.type})"
        for date_off in date_offs
    ]
    name_text = "\n  •".join(list_name)
    text = f"*{type_name}:*\n" + f"  •{name_text}\n  "
    return text


def sync_remain_leave():
    RemainLeaveService.sync_remain_leave()
