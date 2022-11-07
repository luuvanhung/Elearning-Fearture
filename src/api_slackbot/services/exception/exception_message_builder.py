import traceback

from api_slackbot.services.slack.response.base_components_builder import (
    SubComponentBuilder,
)
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from django.conf import settings


def slack_exception_message_builder(error, error_title=None):
    error_detail = error
    if isinstance(error, Exception):
        error_detail = "".join(
            traceback.TracebackException.from_exception(error).format()
        )
        if settings.DEBUG:
            error_detail_blocks = [
                SubComponentBuilder().section_mrkdwn_text_builder(
                    mrkdwn_text=error_detail
                    if error_title is None
                    else f"{error_title}\n{error_detail}"
                )
            ]
        else:
            error_detail_blocks = [
                SubComponentBuilder().section_mrkdwn_text_builder(
                    mrkdwn_text=SlackEnumMessages.ERROR_HAPPENED_MESSAGE
                )
            ]
    else:
        error_detail_blocks = [
            SubComponentBuilder().section_mrkdwn_text_builder(
                mrkdwn_text=error_detail
                if error_title is None
                else f"{error_title}\n{error_detail}"
            )
        ]

    print(
        "-------Error-------\n" + error_detail
        if error_title is None
        else f"{error_title}\n{error_detail}"
    )
    return error_detail_blocks
