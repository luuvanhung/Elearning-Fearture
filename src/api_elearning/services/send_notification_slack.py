from datetime import datetime
from itertools import groupby

from api_base.services.slack import SlackResponseService
from api_elearning.models import Assignment
from api_slackbot.services.slack.response.slack_response_builder import SlackResponseBuilder
from api_user.models import Profile
from django.conf import settings


class SendSlackNotification:
    slack_response_service = SlackResponseService(settings.SLACK_LEAVE_CHANNEL)

    @staticmethod
    def get_channel(
            user: Profile = None,
    ):
        return user.slack_id

    @classmethod
    def send_notification_assignment(cls, assignment: Assignment = None):
        user_profile = assignment.user.profile
        channel = cls.get_channel(user=user_profile)
        response_message = (SlackResponseBuilder.create_notification_assignment(
            assignment=assignment).get("response_blocks"))
        if channel:
            try:
                cls.slack_response_service.send_message(
                    channel=channel,
                    text=response_message[0]['text']['text']
                )
                return None
            except Exception as e:
                return e

    @classmethod
    def send_assignments_reminder(cls, open_assignments=None):
        for user, assignments in groupby(open_assignments, lambda x: x.user):
            user_assignments = dict({
                'user': user,
                'assignments': []
            })
            for assignment in assignments:
                link = f"{settings.URL_WEB_INTERNAL}/my-assignments/{assignment.id}"
                days_left = (assignment.due_date - datetime.now()).days if assignment.due_date else None
                content = dict({
                    'course_title': assignment.course_name,
                    'days_left': days_left,
                    'due_date': str(assignment.due_date),
                    'link_to_course': link
                })
                user_assignments['assignments'].append(content)

            channel = cls.get_channel(user=user_assignments['user'].profile)
            if channel:
                try:
                    response_message = SlackResponseBuilder.send_assignments_reminder(user_assignments)
                    cls.slack_response_service.send_message(
                        channel=channel,
                        text=response_message[0]['text']['text']
                    )
                except Exception as e:
                    print(e)
        return None
