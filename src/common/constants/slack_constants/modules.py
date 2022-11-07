from common.constants.base_const import Const
from core.settings import base


class SlackActionId(Const):
    SELECTED_LEAVE_TYPE = "selected_leave_type"
    BUTTON_CREATED = "created"
    BUTTON_CANCELED = "canceled"
    SELECT_STARTING_DATE = "selected_starting_date"
    SELECT_END_DATE = "selected_end_date"
    SELECT_STARTING_TIME = "selected_starting_time"
    SELECT_END_TIME = "selected_end_time"
    HAVE_LUNCH_CHECKED = "have_lunch_checked"
    BUTTON_CONTINUE_MAKING = "continue_making_duplicate_request"
    BUTTON_NEW_REQUEST = "create_new_request"
    REASON_INPUT = "reason_input"
    BUTTON_APPROVE_REQUEST = "approve_request"
    BUTTON_DENY_REQUEST = "deny_request"
    BUTTON_DELETE_REQUEST = "delete_request"
    BUTTON_CANCEL_DELETE_REQUEST = "cancel_delete_request"


class SlackEvent(Const):
    APP_MENTION = "app_mention"
    CHALLENGE = "challenge"


class SlackResponseHeaderConfig(Const):
    NO_RETRIES = {"X-Slack-No-Retry": 1}


class SlackInputTriggerActionType(Const):
    ON_ENTER_PRESS = "on_enter_pressed"
    ON_CHARACTER_ENTERED = "on_character_entered"


class SlackUrlConstants(Const):
    API_BASE_URL = "https://slack.com/api/"
    CONVERSATION_HISTORY_API = "conversations.history?channel="
    USER_INFO_API = "users.info?user="
    SLACK_BOT_USER_ID = base.SLACK_BOT_USER_ID
