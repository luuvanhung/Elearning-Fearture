class RequestDialogContent:
    DEFAULT_PLACEHOLDER = "Enter your input"

    LEAVE_REQUEST_TITLE = ":nhanmetrai: Are you going to create a leave request?"

    WFH_REQUEST_TITLE = ":nhanmetrai: Are you going to create a work from home request?"

    CANCEL_REQUEST_TITLE = (
        ":nhanmetrai: Are you going to cancel your created leave request?"
    )

    DUPLICATE_REQUEST_MESSAGE = "There is another request on that time!\nWhat you would like to do? :thinking_face:"

    LEAVE_TYPE_SECTION_TITLE = "*Leave type* (_Annual Leave_ as default):"
    LEAVE_TYPE_PLACEHOLDER = "Select leave type"

    REMAIN_LEAVE_TITLE = "*Remain leave allowances:*"

    TAKE_LUNCH_TITLE = "*I want to have lunch!*"
    TAKE_LUNCH_DESCRIPTION = "_No lunch by default._"

    HRM_CREATE_LEAVE_LINK_CONTENT = (
        "Feeling hard to create leave request? Let's try the web UI instead!"
    )
    HRM_CREATE_WFH_LINK_CONTENT = (
        "You can also create a work from home request with the web UI!"
    )
    HRM_CANCEL_LEAVE_LINK_CONTENT = "So complicated? Let's try the web UI instead!"

    CREATE_BUTTON_TEXT = "Create"
    CONFIRM_CREATE_TITLE = "Creating your request"
    CONFIRM_CREATE_TEXT = "Are you sure that you want to create the request?"
    CONFIRM_CREATE_ACTION_TEXT = "Yes, create it!"
    DENY_CREATE_ACTION_TEXT = "No, take me back"

    CANCEL_BUTTON_TEXT = "Cancel"
    CONFIRM_CANCEL_TITLE = "Aborting process"
    CONFIRM_CANCEL_TEXT = "You are going to cancel the request?"
    CONFIRM_CANCEL_ACTION_TEXT = "Yes, abort it!"
    DENY_CANCEL_ACTION_TEXT = "No, keep the process"

    CONTINUE_MAKING_BUTTON_TEXT = "Continue this request"
    CREATE_NEW_BUTTON_TEXT = "Create new one with other time"

    WAITING_LINE_MANAGER_APPROVAL = "_You have to wait for your line manager's permission to be off as you requested_ :troll:"
    NO_NEED_LINE_MANAGER_APPROVE = "_Because you don't have line manger so your request will be automatically approved_ :pepeok:"

    NEW_LEAVE_REQUEST_TITLE = (
        "You have a new leave request that is waiting for your permission!"
    )

    DELETE_REQUEST_BUTTON_TEXT = "Delete"
    CONFIRM_DELETE_TITLE = "Deleting your request"
    CONFIRM_DELETE_TEXT = "Are you sure that you want to delete this request?"
    CONFIRM_DELETE_ACTION_TEXT = "I'm sure"
    DENY_DELETE_ACTION_TEXT = "No, take me back"

    CANCEL_DELETE_REQUEST_BUTTON_TEXT = "Cancel"
    CONFIRM_CANCEL_DELETE_REQUEST_TITLE = "Aborting process"
    CONFIRM_CANCEL_DELETE_REQUEST_TEXT = (
        "You are going to cancel deleting request process?"
    )
    CONFIRM_CANCEL_DELETE_REQUEST_ACTION_TEXT = "Yes, abort it!"
    DENY_CANCEL_DELETE_REQUEST_ACTION_TEXT = "No, keep the process"

    SOME_REQUEST_NOT_IN_LIST_NOTE = "_*Some of your requests may not in this list because they're expired to be canceled._"
    DELETE_REQUEST_PREFACE_SENTENCE = (
        "_*Here are all your pending leave requests, please choose one!*_"
    )
    NO_PENDING_REQUEST_AVAILABLE = "*All your requests are expired or have been actioned by line-manager.* \n _Create a new one to cancel it :troll:_"

    DELETED_REQUEST_RESPONSE_TITLE = "You have just deleted this request :raised_hands:"

    CANCEL_LEAVE_REQUEST_TITLE = "Cancel leave request"
    APPROVE_CANCEL_LEAVE_REQUEST_TITLE = "Approve Cancel leave request"
    REJECT_CANCEL_LEAVE_REQUEST_TITLE = "Reject Cancel leave request"


class NotificationDialogContent:
    APPROVE_BUTTON_TEXT = "Approve"
    CONFIRM_APPROVE_TITLE = "Approve request"
    CONFIRM_APPROVE_TEXT = "Are you sure that you want to approve this request?"
    CONFIRM_APPROVE_ACTION_TEXT = "Yes, I approve"
    CANCEL_APPROVE_ACTION_TEXT = "No, don't approve it!"

    DENY_BUTTON_TEXT = "Deny"
    CONFIRM_DENY_TITLE = "Deny request"
    CONFIRM_DENY_TEXT = "You're about to deny an employee leave request!"
    CONFIRM_DENY_ACTION_TEXT = "Deny this request"
    CANCEL_DENY_ACTION_TEXT = "No, take me back!"

    APPROVED_RESPONSE_TITLE = "You approved the request :nhanmetrai:"
    DENIED_RESPONSE_TITLE = "You denied the request :relieved: :relieved:"

    HRM_APPROVAL_LINK_CONTENT = (
        "You can make decision about this request with the web UI"
    )
    HRM_APPROVAL_MEMBER_LINK_CONTENT = "Check the UI web for more information!"
