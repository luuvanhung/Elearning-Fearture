import json
import threading

from api_base.services.slack.service import SlackResponseService, SlackWebhookService
from api_slackbot.services.exception.exception_engine_builder import InteractingExceptionEngine, MentionExceptionEngine
from api_slackbot.services.exception.exception_handler import ExceptionHandler
from api_slackbot.services.exception.exception_message_builder import slack_exception_message_builder
from api_slackbot.services.nlp.predictions import get_transferred_prediction
from api_slackbot.services.slack.interactive_components_handler.line_manager_action_service import (
    LineManagerActionService,
)
from api_slackbot.services.slack.response.base_components_builder import SubComponentBuilder
from api_slackbot.services.slack.response.slack_response_builder import SlackResponseBuilder
from api_slackbot.services.slack.user_request.handler import UserLeaveRequestHandler, UserWFHRequestHandler
from api_slackbot.services.slack.users_api.user_info import SlackUserInfoService
from api_slackbot.services.temp_leave_request.temp_leave_request_service import TempLeaveRequestService
from api_user.services.profile import ProfileService
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.services.action_request import ActionRequestService
from api_workday.services.leave_type import LeaveTypeService
from api_workday.services.remain_leave import RemainLeaveService
from api_workday.services.request_off import RequestOffServices
from common.constants.slack_constants import SlackTextMessage
from common.constants.slack_constants.enum_messages import SlackEnumMessages
from common.constants.slack_constants.modules import (
    SlackActionId,
    SlackEvent,
    SlackResponseHeaderConfig,
    SlackUrlConstants,
)
from common.constants.wit_constants import WitIntent
from common.constants.workday_constants.date import Workday
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.datetime_utils import date_string_to_datetime


def get_profile_by_slack_id_and_update_if_missing(user_slack_id):
    # Get user email
    user_email = SlackUserInfoService().get_user_email_by_slack_id(
        user_slack_id=user_slack_id
    )

    # Get user profile from HRM by user email, using super admin for quicker testing
    profile = ProfileService.get_profile_by_email(personal_email=user_email)
    if profile is None:
        return None
    elif profile.slack_id is None or len(profile.slack_id.strip()) <= 0:
        ProfileService.update_slack_id_by_profile_id(
            profile_id=profile.id, slack_id=user_slack_id
        )
    return profile


def handling_if_profile_not_existed(exception_handler):
    none_profile_exception_blocks = [
        SubComponentBuilder().section_mrkdwn_text_builder(
            mrkdwn_text=SlackEnumMessages.USER_NOT_FOUND_MESSAGE
        )
    ]
    return exception_handler.send_exception_blocks(
        none_profile_exception_blocks
    ).return_http_no_retires_response("User not found")


def handling_if_no_manager_and_no_maximum_level(exception_handler):
    none_permission_exception_blocks = [
        SubComponentBuilder().section_mrkdwn_text_builder(
            mrkdwn_text=SlackEnumMessages.NO_MANAGER_AND_MAXIMUM_LEVEL
        )
    ]
    return exception_handler.send_exception_blocks(
        none_permission_exception_blocks
    ).return_http_no_retires_response("No permission")


def create_temp_leave_request_and_send_response(
    transferred_intents,
    channel_id,
    slack_user_id,
    profile,
    lunch_status=False,
    full_day_leave_lunch_flag=False,
    exception_engine=None,
    slack_service=None,
):
    if slack_service is None:
        slack_service = SlackResponseService(channel=channel_id)

    # Initial the exception handler
    if exception_engine is None:
        exception_engine = MentionExceptionEngine(slack_service, slack_user_id)

    existed_request = (
        TempLeaveRequestService.get_temp_leave_request_by_profile_id_and_from_datetime(
            profile_id=profile.id,
            from_date=transferred_intents.get("date_time").get("from_date"),
            from_time=transferred_intents.get("date_time").get("from_time"),
        )
    )

    # Check if request already existed with same requested date!!!
    if existed_request is not None:
        # Creating response to duplicated request
        response_to_duplicated_request = (
            SlackResponseBuilder.create_duplicate_request_response(
                existed_request.id, transferred_intents.get("text")
            )
        )

        if response_to_duplicated_request.get("is_exception"):
            return exception_engine.send_exception_blocks(
                response_to_duplicated_request.get("response_blocks")
            ).return_http_no_retires_response(SlackEnumMessages.EXCEPTION_RAISED)
        else:
            # Send Slack response for duplicate request
            slack_service.send_ephemeral_message(
                user=slack_user_id,
                text="Your request already existed",
                blocks=response_to_duplicated_request.get("response_blocks"),
            )

            return Response(
                dict(msg=SlackEnumMessages.SENT_SUCCESSFULLY_TO_USER),
                status=status.HTTP_200_OK,
                headers=SlackResponseHeaderConfig.NO_RETRIES,
            )

    if transferred_intents.get("user_intent") != WitIntent.CREATE_WFH_REQUEST:
        default_leave_type = (
            LeaveTypeService.get_longest_duration_and_is_company_pay_leave_type()
        )
    # Because WFH does not count as a leave type, so we save the field
    # leave_type_id = None for a wfh request
    else:
        default_leave_type = {"id": None}

    temp_leave_request_id = TempLeaveRequestService.create_temp_leave_request(
        profile_id=profile.id,
        request_date=transferred_intents.get("date_time"),
        lunch_status=lunch_status,
        full_day_leave_lunch_flag=full_day_leave_lunch_flag,
        reason=transferred_intents.get("reason"),
        leave_type_id=default_leave_type.get("id"),
    )

    remain_leaves = RemainLeaveService.retrieve_remain_leaves(profile).get(
        "current_days_off"
    )

    # Creating response
    response_to_valid_request = SlackResponseBuilder.create_valid_request_response(
        transferred_intents=transferred_intents,
        remain_leaves=remain_leaves,
        temp_leave_request_id=temp_leave_request_id,
        default_leave_type=default_leave_type,
    )
    if response_to_valid_request.get("is_exception"):
        return (
            exception_engine.send_exception_blocks(
                response_to_valid_request.get("response_blocks")
            )
            .call_delete_temp_request_by_id_service(temp_leave_request_id)
            .return_http_no_retires_response(SlackEnumMessages.EXCEPTION_RAISED)
        )
    else:
        # Send Slack response if valid
        slack_service.send_ephemeral_message(
            user=slack_user_id,
            text=SlackTextMessage.HERE_IS_YOUR_REQUEST,
            blocks=response_to_valid_request.get("response_blocks"),
        )

        return Response(
            dict(msg=SlackEnumMessages.SENT_SUCCESSFULLY_TO_USER),
            status=status.HTTP_200_OK,
            headers=SlackResponseHeaderConfig.NO_RETRIES,
        )


def cancel_leave_request_and_response(
    profile, slack_user_id, exception_engine, slack_service
):
    current_date = timezone.now().astimezone().date()
    pending_request_off_queryset = RequestOffServices.get_pending_request_off(
        profile.id
    )
    pending_request_off_serializer = RequestOffSerializer(
        pending_request_off_queryset, many=True
    )
    pending_request_off = [
        request_off
        for request_off in pending_request_off_serializer.data
        if date_string_to_datetime(request_off.get("date_off")[-1].get("date"))
        >= current_date
    ]

    response_to_canceling_request = (
        SlackResponseBuilder.create_canceling_leave_request_response(
            pending_request_off
        )
    )

    if response_to_canceling_request.get("is_exception"):
        return exception_engine.send_exception_blocks(
            response_to_canceling_request.get("response_blocks")
        ).return_http_no_retires_response(SlackEnumMessages.EXCEPTION_RAISED)
    else:
        slack_service.send_ephemeral_message(
            user=slack_user_id,
            text=SlackTextMessage.HERE_IS_YOUR_REQUEST,
            blocks=response_to_canceling_request.get("response_blocks"),
        )
        return Response(
            dict(msg=SlackEnumMessages.SENT_SUCCESSFULLY_TO_USER),
            status=status.HTTP_200_OK,
            headers=SlackResponseHeaderConfig.NO_RETRIES,
        )


def handling_mention_request(request_data):
    message_data = request_data.get("event")
    slack_requesting_user_id = message_data.get("user")
    # Using another thread for logic handling
    slack_response_service = SlackResponseService(
        channel=request_data.get("event").get("channel")
    )

    # GET USER PROFILE BY EMAIL, NOT SLACK_ID!!!!!!!!
    profile = get_profile_by_slack_id_and_update_if_missing(
        user_slack_id=slack_requesting_user_id
    )

    # Initial the exception handler
    mention_exception_engine = MentionExceptionEngine(
        slack_response_service, slack_requesting_user_id
    )

    if profile is None:
        return handling_if_profile_not_existed(mention_exception_engine)
    elif profile.line_manager_id is None and profile.maximum_level_approved != 0:
        return handling_if_no_manager_and_no_maximum_level(mention_exception_engine)

    slack_response_service.send_ephemeral_message(
        user=slack_requesting_user_id,
        text=SlackEnumMessages.WAITING_MESSAGE,
    )

    transferred_intents = get_transferred_prediction(message_data.get("text"))

    if transferred_intents.get("is_exception"):
        return mention_exception_engine.send_exception_blocks(
            transferred_intents.get("response_blocks")
        ).return_http_no_retires_response(SlackEnumMessages.EXCEPTION_RAISED)

    if message_data.get("type") == SlackEvent.APP_MENTION and (
        slack_requesting_user_id is not SlackUrlConstants.SLACK_BOT_USER_ID
        or message_data.get("bot_id") is None
    ):
        if (
            transferred_intents.get("user_intent") == WitIntent.CREATE_LEAVE_REQUEST
            or transferred_intents.get("user_intent") == WitIntent.CREATE_WFH_REQUEST
        ):
            try:
                return create_temp_leave_request_and_send_response(
                    transferred_intents=transferred_intents,
                    channel_id=message_data.get("channel"),
                    slack_user_id=slack_requesting_user_id,
                    profile=profile,
                    exception_engine=mention_exception_engine,
                    slack_service=slack_response_service,
                )
            except Exception as e:
                return ExceptionHandler(
                    e, mention_exception_engine
                ).default_exception_when_creating_request(
                    profile_id=profile.id,
                    from_date=transferred_intents.get("date_time").get("from_date"),
                    from_time=transferred_intents.get("date_time").get("from_time"),
                )

        if transferred_intents.get("user_intent") == WitIntent.CANCEL_LEAVE_REQUEST:
            try:
                return cancel_leave_request_and_response(
                    profile=profile,
                    slack_user_id=slack_requesting_user_id,
                    exception_engine=mention_exception_engine,
                    slack_service=slack_response_service,
                )
            except Exception as e:
                return ExceptionHandler(
                    e, mention_exception_engine
                ).exception_when_call_canceling_request()


def handling_action_event(request):
    scopes = request.auth.scopes
    request_data = json.loads(request.data.get("payload"))
    slack_requesting_user_id = request_data.get("user").get("id")
    action_data = request_data.get("actions")[0]
    user_action = json.loads(action_data.get("action_id"))
    slack_webhook_service = SlackWebhookService(request_data.get("response_url"))
    # Initial the exception handler
    interacting_exception_engine = InteractingExceptionEngine(
        slack_webhook_service, slack_requesting_user_id
    )

    # GET USER PROFILE BY EMAIL, NOT SLACK_ID!
    profile = get_profile_by_slack_id_and_update_if_missing(
        user_slack_id=slack_requesting_user_id
    )

    if profile is None:
        return handling_if_profile_not_existed(interacting_exception_engine)

    try:
        # CATCH THE CANCEL BUTTON EVENT: user canceled the request then not any actions triggered
        if user_action.get("action_type") == SlackActionId.BUTTON_CANCELED:
            TempLeaveRequestService.delete_temp_leave_request_if_exist_by_id(
                user_action.get("temp_leave_request_id")
            )
            slack_webhook_service.send_response_to_interacting(
                text="*Canceled* :pepeok:"
            )
            return

        # CATCH THE CANCEL DELETING REQUEST BUTTON EVENT
        if user_action.get("action_type") == SlackActionId.BUTTON_CANCEL_DELETE_REQUEST:
            slack_webhook_service.send_response_to_interacting(
                text="*Canceled* :pepeok:"
            )
            return

        # CATCH THE CREATE NEW REQUEST WIT DIFFERENT DATE BUTTON EVENT:
        if user_action.get("action_type") == SlackActionId.BUTTON_NEW_REQUEST:
            slack_webhook_service.send_response_to_interacting(
                text=SlackEnumMessages.CREATE_NEW_WITH_DIFFERENT_DATE_MESSAGE
            )
            return

        # CATCH THE DELETE REQUEST BUTTON EVENT:
        if user_action.get("action_type") == SlackActionId.BUTTON_DELETE_REQUEST:
            deleted_request = ActionRequestService.do_action_request(
                request_data=dict(
                    request_off_id=user_action.get("request_off_id"),
                    comment="Cancel Request",
                    action=Workday.STATUS_CANCELED,
                ),
                profile=profile,
                scopes = scopes
            )
            if deleted_request is not None:
                response_to_canceled_request = (
                    SlackResponseBuilder.create_canceled_request_response(
                        deleted_request
                    )
                )
                if response_to_canceled_request.get("is_exception"):
                    interacting_exception_engine.send_exception_blocks(
                        slack_exception_message_builder(
                            response_to_canceled_request.get("response_blocks")
                        )
                    )
                else:
                    slack_webhook_service.send_response_to_interacting(
                        text="Request deleted!",
                        blocks=response_to_canceled_request.get("response_blocks"),
                    )
            return
    except Exception as e:
        return interacting_exception_engine.send_exception_blocks(
            slack_exception_message_builder(e)
        )

    try:
        # CATCH LINE MANAGER APPROVE REQUEST EVENT:
        if user_action.get("action_type") == SlackActionId.BUTTON_APPROVE_REQUEST:
            return LineManagerActionService(
                request_off_id=user_action.get("request_off_id"),
                slack_service=slack_webhook_service,
                slack_exception_engine=interacting_exception_engine,
                profile=profile,
                list_dates=json.loads(action_data.get("value")).get("list_dates"),
            ).action_handling(line_manager_action_type=Workday.STATUS_APPROVED, scopes=scopes)

        # CATCH LINE MANAGER DENY REQUEST EVENT:
        if user_action.get("action_type") == SlackActionId.BUTTON_DENY_REQUEST:
            return LineManagerActionService(
                request_off_id=user_action.get("request_off_id"),
                slack_service=slack_webhook_service,
                slack_exception_engine=interacting_exception_engine,
                profile=profile,
                list_dates=json.loads(action_data.get("value")).get("list_dates"),
            ).action_handling(line_manager_action_type=Workday.STATUS_REJECTED, scopes=scopes)
    except Exception as e:
        return ExceptionHandler(
            e, interacting_exception_engine
        ).line_manager_action_exception()

    # Find temp_leave_request in temp table by id
    temp_leave_request = TempLeaveRequestService.get_temp_leave_request_by_id(
        user_action.get("temp_leave_request_id")
    )

    try:
        # Handle case: temp_leave_request is None but still have action triggered
        if temp_leave_request is None and (
            user_action.get("action_type") != SlackActionId.BUTTON_CONTINUE_MAKING
        ):
            temp_empty_exception_block = [
                SubComponentBuilder().section_mrkdwn_text_builder(
                    mrkdwn_text=SlackEnumMessages.REQUEST_NOT_FOUND_MESSAGE
                )
            ]
            return interacting_exception_engine.send_exception_blocks(
                temp_empty_exception_block
            ).return_http_no_retires_response("Temp leave request not found!")

        # CATCH THE SELECTING LEAVE TYPE EVENT
        if user_action.get("action_type") == SlackActionId.SELECTED_LEAVE_TYPE:
            TempLeaveRequestService.update_leave_type_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                leave_type_id=action_data.get("selected_option").get("value"),
            )

        # CATCH THE SELECTING STARTING DATE EVENT
        if user_action.get("action_type") == SlackActionId.SELECT_STARTING_DATE:
            TempLeaveRequestService.update_from_date_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                selected_date=action_data.get("selected_date"),
            )

        # CATCH THE SELECTING STARTING TIME EVENT, LUNCH STATUS=FALSE IF NOT HALF-DAY LEAVE
        if user_action.get("action_type") == SlackActionId.SELECT_STARTING_TIME:
            TempLeaveRequestService.update_from_time_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                selected_time=action_data.get("selected_option").get("value"),
            )

        # CATCH THE SELECTING END DATE EVENT
        if user_action.get("action_type") == SlackActionId.SELECT_END_DATE:
            TempLeaveRequestService.update_to_date_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                selected_date=action_data.get("selected_date"),
            )

        # CATCH THE SELECTING END TIME EVENT, LUNCH STATUS=FALSE IF NOT HALF-DAY LEAVE
        if user_action.get("action_type") == SlackActionId.SELECT_END_TIME:
            TempLeaveRequestService.update_to_time_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                selected_time=action_data.get("selected_option").get("value"),
            )

        # CATCH THE REASON INPUT EVENT
        if user_action.get("action_type") == SlackActionId.REASON_INPUT:
            TempLeaveRequestService.update_reason_by_id(
                temp_leave_request_id=user_action.get("temp_leave_request_id"),
                reason=action_data.get("value"),
            )

        # CATCH THE HAVE LUNCH CHECKED EVENT
        if user_action.get("action_type") == SlackActionId.HAVE_LUNCH_CHECKED:
            if len(action_data.get("selected_options")) < 1:
                TempLeaveRequestService.update_lunch_status_by_id(
                    temp_leave_request_id=user_action.get("temp_leave_request_id"),
                    value=False,
                )
            else:
                TempLeaveRequestService.update_lunch_status_by_id(
                    temp_leave_request_id=user_action.get("temp_leave_request_id"),
                    value=True,
                )

        # CATCH THE CONFIRM BUTTON EVENT
        if user_action.get("action_type") == SlackActionId.BUTTON_CREATED:
            """
            button_values = {
                "action": ,
                "from": ,
                "to": ,
                "quantity": ,
                "reason":
            }
            """
            button_values = json.loads(action_data.get("value"))

            # Map to service.
            # Because the WFH is not a leave type, so it does not have
            # ID in DB (consider this later)
            if button_values.get("type") == Workday.WFH:
                user_wfh_request_handler = UserWFHRequestHandler(
                    slack_webhook_service,
                    button_values,
                    profile,
                    temp_leave_request,
                    interacting_exception_engine,
                )
                return user_wfh_request_handler.handling()

            else:
                user_leave_request_handler = UserLeaveRequestHandler(
                    slack_webhook_service,
                    button_values,
                    profile,
                    temp_leave_request,
                    interacting_exception_engine,
                )
                return user_leave_request_handler.handling()

        # CATCH THE CONTINUE-MAKING BUTTON EVENT:
        if user_action.get("action_type") == SlackActionId.BUTTON_CONTINUE_MAKING:
            TempLeaveRequestService.delete_temp_leave_request_if_exist_by_id(
                user_action.get("temp_leave_request_id")
            )
            slack_webhook_service.send_response_to_interacting(
                text=SlackEnumMessages.GET_LAST_REQUEST_MESSAGE
            )
            return create_temp_leave_request_and_send_response(
                transferred_intents=get_transferred_prediction(
                    user_action.get("user_message")
                ),
                channel_id=request_data.get("channel").get("id"),
                slack_user_id=slack_requesting_user_id,
                profile=profile,
            )
    except Exception as e:
        return ExceptionHandler(
            e, interacting_exception_engine
        ).default_exception_when_creating_request(
            temp_leave_request_id=temp_leave_request.id.hex
        )


class SlackMessageHandler(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        request_data = request.data
        if SlackEvent.CHALLENGE in request_data:
            return Response(
                {"challenge": request_data.get("challenge")}, status=status.HTTP_200_OK
            )
        else:
            mention_event_thread = threading.Thread(
                target=handling_mention_request, args=([request_data])
            )
            mention_event_thread.start()
            # Making immediately response for slack to know that we received the request and do not need to retry.
            # for more information, read this: https://api.slack.com/apis/connections/events-api#errors
            return Response(
                status=status.HTTP_200_OK, headers=SlackResponseHeaderConfig.NO_RETRIES
            )


class SlackInteractiveComponentsHandler(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        action_event_thread = threading.Thread(
            target=handling_action_event, args=([request])
        )
        action_event_thread.start()
        # Making immediately response for slack to know that we received the request and do not need to retry.
        # for more information, read this: https://api.slack.com/apis/connections/events-api#errors
        return Response(
            status=status.HTTP_200_OK, headers=SlackResponseHeaderConfig.NO_RETRIES
        )
