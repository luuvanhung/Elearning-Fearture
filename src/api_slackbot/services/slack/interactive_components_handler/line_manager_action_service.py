from api_slackbot.services.exception.exception_handler import ExceptionHandler
from api_slackbot.services.slack.response import SlackResponseBuilder
from api_user.services.profile import ProfileService
from api_workday.models.request_detail import RequestDetail
from api_workday.services.action_request import ActionRequestService
from api_workday.services.request_off import RequestOffServices
from common.constants.slack_constants.dialog_content import NotificationDialogContent
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from common.constants.workday_constants.date import Workday
from django.conf import settings


class LineManagerActionService:
    def __init__(
        self, request_off_id, slack_service, profile, slack_exception_engine, list_dates
    ):
        self.request_off = RequestOffServices.get_request_off_by_id(request_off_id)
        self.slack_exception_engine = slack_exception_engine
        self.slack_service = slack_service
        self.list_dates = list_dates

        self.profile = (
            ProfileService.get_profile_by_slack_id(
                settings.DEV_LINE_MANAGER_SLACK_USER_ID
            )
            if settings.ENVIRONMENT == "dev"
            else profile
        )

    def message_response_builder(self, title):
        return SlackResponseBuilder.create_line_manager_actioned_response(
            profile=self.profile,
            title=title,
            list_dates=self.list_dates,
            leave_type_id=self.request_off.leave_type_id,
            request_off_reason=self.request_off.reason,
            request_off_total=self.request_off.total,
        )

    def action_handling(self, line_manager_action_type, scopes):
        if self.request_off is not None:
            request_detail = RequestDetail.objects.filter(
                request_off_id=self.request_off.id, approve=self.profile
            ).first()
            if request_detail is not None:
                if self.request_off.status == Workday.STATUS_PENDING:
                    try:
                        actioned_request = ActionRequestService.do_action_request(
                            request_data=dict(
                                request_off_id=self.request_off.id,
                                comment="null",
                                action=line_manager_action_type,
                            ),
                            profile=self.profile,
                            scopes=scopes,
                        )

                        if actioned_request is not None:
                            actioned_response_message = self.message_response_builder(
                                NotificationDialogContent.DENIED_RESPONSE_TITLE
                            )
                            slack_text = "Request rejected!"

                            if line_manager_action_type == Workday.STATUS_APPROVED:
                                actioned_response_message = self.message_response_builder(
                                    NotificationDialogContent.APPROVED_RESPONSE_TITLE
                                )
                                slack_text = "Request approved!"

                            self.slack_service.send_response_to_interacting(
                                text=slack_text,
                                blocks=actioned_response_message.get("response_blocks"),
                            )

                        else:
                            ExceptionHandler(
                                error="Some error occurred under the hood of HRM, "
                                "please contact developer to fix it!",
                                exception_engine=self.slack_exception_engine,
                            ).line_manager_action_exception()

                    except Exception as e:
                        ExceptionHandler(
                            error=e, exception_engine=self.slack_exception_engine
                        ).line_manager_action_exception()

                elif (
                    self.request_off.status == Workday.STATUS_APPROVED
                    or self.request_off.status == Workday.STATUS_REJECTED
                ):
                    ExceptionHandler(
                        error=SlackEnumMessages.REQUEST_ACTIONED,
                        exception_engine=self.slack_exception_engine,
                    ).line_manager_action_exception()
                elif self.request_off.status == Workday.STATUS_CANCELED:
                    ExceptionHandler(
                        error=SlackEnumMessages.REQUEST_CANCELED,
                        exception_engine=self.slack_exception_engine,
                    ).line_manager_action_exception()
            else:
                ExceptionHandler(
                    error=SlackEnumMessages.NOT_LINE_MANAGER,
                    exception_engine=self.slack_exception_engine,
                ).line_manager_action_exception()
        else:
            ExceptionHandler(
                error=SlackEnumMessages.EMPLOYEE_REQUEST_NOT_FOUND_OR_ERROR,
                exception_engine=self.slack_exception_engine,
            ).line_manager_action_exception()
