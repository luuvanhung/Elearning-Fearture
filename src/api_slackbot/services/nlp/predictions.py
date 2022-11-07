from api_slackbot.services.exception.exception_message_builder import (
    slack_exception_message_builder,
)
from api_slackbot.services.slack.response.base_components_builder import (
    SubComponentBuilder,
)
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from common.constants.wit_constants import WitIntent
from common.constants.wit_constants.modules import WitModules
from django.conf import settings
from nlp_knowledge_base.base import NlpService
from nlp_knowledge_base.services.wit.data_process import (
    CancelLeaveRequestParser,
    CreateLeaveRequestParser,
)


# Call NPL service and get result
def get_transferred_prediction(message):
    try:
        user_text_message = message.replace(
            "<@" + settings.SLACK_BOT_USER_ID + ">", ""
        ).strip()

        if len(user_text_message) >= 250 or len(user_text_message) <= 5:
            error_detail_blocks = slack_exception_message_builder(
                error="*Your message must be grater than 5 and less than or equal 250 characters* :pepeknife:"
            )
            return {
                "is_exception": True,
                "response_blocks": error_detail_blocks,
            }

        wit_response = (
            NlpService(engine_name=WitModules.NAME, access_token=settings.WIT_TOKEN)
            .get_engine()
            .get_intents(message=user_text_message)
            .returned_intents
        )

        if "error" in wit_response:
            error_detail_blocks = slack_exception_message_builder(
                error="Wit's service: " + wit_response.get("error")
            )
            return {
                "is_exception": True,
                "response_blocks": error_detail_blocks,
            }

        if wit_response.get("intents"):
            if wit_response.get("intents")[0].get("confidence") > float(
                settings.INTENT_THRESHOLD
            ):
                predicted_intent = wit_response.get("intents")[0]
                # Parse with create_leave
                if (
                    predicted_intent.get("name") == WitIntent.CREATE_LEAVE_REQUEST
                    or predicted_intent.get("name") == WitIntent.CREATE_WFH_REQUEST
                ):
                    return (
                        CreateLeaveRequestParser(wit_response)
                        .get_text()
                        .get_sentence_intent(intent_name=predicted_intent.get("name"))
                        .get_date_time()
                        .get_user_reason()
                        .intents_data_transfer_object
                    )
                # Parse with cancel_leave
                elif predicted_intent.get("name") == WitIntent.CANCEL_LEAVE_REQUEST:
                    return (
                        CancelLeaveRequestParser(wit_response)
                        .get_text()
                        .get_sentence_intent(intent_name=WitIntent.CANCEL_LEAVE_REQUEST)
                        .get_date_time()
                        .intents_data_transfer_object
                    )
                else:
                    return {
                        "is_exception": True,
                        "response_blocks": [
                            SubComponentBuilder().section_mrkdwn_text_builder(
                                mrkdwn_text=SlackEnumMessages.UN_IMPLEMENT_INTENT
                            )
                        ],
                    }
            return {
                "is_exception": True,
                "response_blocks": [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=SlackEnumMessages.NOOB_MESSAGE
                    )
                ],
            }
        # Handling case: if no intents were found
        else:
            return {
                "is_exception": True,
                "response_blocks": [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=SlackEnumMessages.NOOB_MESSAGE
                    )
                ],
            }

    except Exception as e:
        exception_blocks = slack_exception_message_builder(e)
        return {
            "is_exception": True,
            "response_blocks": exception_blocks,
        }
