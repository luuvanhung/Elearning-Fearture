from api_slackbot.services.temp_leave_request.temp_leave_request_service import (
    TempLeaveRequestService,
)
from common.constants.slack_constants.modules import SlackResponseHeaderConfig
from rest_framework import status
from rest_framework.response import Response


class SlackBaseExceptionEngine:
    def __init__(self, slack_user_id, slack_service=None):
        self.service = slack_service
        self.slack_user_id = slack_user_id
        self.error = ""

    def call_delete_temp_request_by_profile_id_service(self, profile_id):
        TempLeaveRequestService.delete_temp_leave_request_if_exist_by_profile_id(
            profile_id
        )
        return self

    def call_delete_temp_request_by_profile_id_and_from_datetime_service(
        self, profile_id, from_date, from_time
    ):
        TempLeaveRequestService.delete_temp_leave_request_if_exist_by_profile_id_and_from_datetime(
            profile_id=profile_id, from_date=from_date, from_time=from_time
        )
        return self

    def call_delete_temp_request_by_id_service(self, temp_leave_request_id):
        TempLeaveRequestService.delete_temp_leave_request_if_exist_by_id(
            temp_leave_request_id
        )
        return self

    @staticmethod
    def return_http_no_retires_response(error):
        return Response(
            dict(msg=error),
            status=status.HTTP_200_OK,
            headers=SlackResponseHeaderConfig.NO_RETRIES,
        )


class MentionExceptionEngine(SlackBaseExceptionEngine):
    def __init__(self, slack_response_service, slack_user_id):
        super().__init__(slack_user_id, slack_service=slack_response_service)

    def send_exception_blocks(self, exception_blocks):
        self.service.send_ephemeral_message(
            user=self.slack_user_id,
            text="Some bad things may happened!",
            blocks=exception_blocks,
        )
        return self


class InteractingExceptionEngine(SlackBaseExceptionEngine):
    def __init__(self, slack_webhook_service, slack_user_id):
        super().__init__(slack_user_id, slack_service=slack_webhook_service)

    def send_exception_blocks(self, exception_blocks):
        self.service.send_response_to_interacting(
            text="Some bad things may happened!", blocks=exception_blocks
        )
        return self


class SendingNotificationExceptionEngine(SlackBaseExceptionEngine):
    def __init__(self, slack_response_service, slack_user_id):
        super().__init__(slack_user_id, slack_service=slack_response_service)

    def send_exception_blocks(self, exception_text, exception_blocks):
        self.service.send_message(
            user=self.slack_user_id,
            text=exception_text,
            blocks=exception_blocks,
        )
        return self
