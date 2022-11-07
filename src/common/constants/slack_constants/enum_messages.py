class SlackEnumMessages:
    NOOB_MESSAGE = "Okay, I'm noob :crying: please make your sentence more clearly, or check again your typo!"
    UN_IMPLEMENT_INTENT = "This intent's handler has not implemented!"
    USER_NOT_FOUND_MESSAGE = ":no_entry_sign: *Can not found you in system*\n_Please contact manager to know more!_"
    NO_MANAGER_AND_MAXIMUM_LEVEL = ":no_entry_sign: *You don't have any line manger, neither the maximum level!*\n_Please contact manager to know more!_"
    ERROR_HAPPENED_MESSAGE = (
        ":no_entry_sign: Some bad things happened, contact the developers to fix it!"
    )
    ONLY_WEEKEND_MESSAGE = "I'm smart enough to know that it's only weekend day, don't underestimate me! :pepeknife:"

    DUPLICATE_REQUEST_MESSAGE = ":warning: *There is another request on that time!* :warning:\n*What you would like to do?*"

    CREATE_NEW_WITH_DIFFERENT_DATE_MESSAGE = (
        "*Let's create new request with another time!* :wink:"
    )
    GET_LAST_REQUEST_MESSAGE = "*Just hold my :beers: I'm getting your last request!*"

    WAITING_MESSAGE = "*Just hold my :beers: I'm getting your intent!*"

    REQUEST_NOT_FOUND_MESSAGE = "*Your session is timeout!* \nPlease create a new one!"
    INVALID_QUANTITY_DAYS_MESSAGE = "Invalid quantity of requested leave days!"
    INVALID_END_DATE_MESSAGE = (
        "End date must not be smaller than the starting date! :pepeknife:"
    )
    ONE_FOR_HALF_DAY_ONLY_MESSAGE = (
        "Half-day leave can only be created for only one day per request!"
    )

    REQUEST_ACTIONED = (
        ":no_entry_sign: *This request has been approved or rejected!* :no_entry_sign:"
    )
    REQUEST_CANCELED = (
        "*:no_entry_sign: This request has been canceled by the owner! :no_entry_sign:*"
    )
    NOT_LINE_MANAGER = "*Can not action because you are not the line manager of this request's employee!* :hidepain:"

    EMPLOYEE_REQUEST_NOT_FOUND_OR_ERROR = (
        ":no_entry_sign: *This employee's request is not exist in the system or*\n"
        "*maybe some bad things happened, contact the developers to fix it!*"
    )
    YOUR_REQUEST_HAS_BEEN_APPROVED = "Your request has been approved :nhanmetrai:"
    YOUR_REQUEST_HAS_BEEN_REJECTED = "Your request has been rejected :hidepain:"
    ERROR_WHEN_SENDING_NOTICE_ABOUT_CANCEL_LEAVE_REQUEST = "Error when send notice about cancel leave request!"
    EXCEPTION_RAISED = "Exception raised, please contact the developers to fix it!"
    SENT_SUCCESSFULLY_TO_USER = "Sent successfully to requesting user"


class SlackTextMessage:
    ERROR_WHEN_SENDING_NEW_LEAVE_REQUEST_NOTIFICATION = "Error when sending you new leave request notification!"
    ERROR_WHEN_SENDING_TO_YOU_NOTIFICATION_REJECTED_LEAVE_REQUEST = "Error when sending you notification about your rejected leave request!"
    NEW_LEAVE_REQUEST = "New leave request!"
    SOME_TEAM_MEMBERS_WILL_NOT_GO_TO_THE_OFFICE_TODAY = "Some team members will not go to the office today!"
    ERROR_WHEN_SENDING_TO_TEAM_NOTIFICATION_NEW_APPROVED_REQUEST = "Error when sending to team notification about new approved leave request!"
    ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_APPROVED_REQUEST = "Error with employee notification with their approved request!"
    ERROR_WHEN_SENDING_TO_EMPLOYEE_NOTIFICATION_NEW_REJECTED_REQUEST = "Error with employee notification with their rejected request!"
    ERROR_WHEN_SENDING_TO_LUNCH_MANAGER_NOTIFICATION = "Error when sending notification about lunch!"
    REQUEST_APPROVED = "Request approved!"
    REQUEST_REJECTED = "Request rejected!"
    HERE_IS_YOUR_REQUEST = "Here is your request information!"


class SlackBlocksMessage:
    ERROR_WHEN_SENDING_TO_APPROVER_NOTIFICATION_NEW_LEAVE_REQUEST = "Error when sending to approver notification about new leave request!"
    ERROR_WHEN_SENDING_TO_LUNCH_MANAGER_NOTIFICATION = "Error when sending lunch manager notification about lunch information!",


class FormLeaveRequest:
    CREATE_LEAVE_REQUEST = "*Created leave request* :nhanmetrai:\n"
    NAME = ":point_right: Name: *"
    TEAMS = ":point_right: Teams: *"
    DURATION = ":point_right: Duration: *"
    TO = "* to *"
    QUANTITY = ":point_right: Quantity: *"
    LEAVE_TYPE = ":point_right: Leave Type: *"
    REASON = ":point_right: Reason: *"
    NO_DATA = " *_No data_*"
    HAVING_LUNCH = ":point_right: Having lunch: *"


class NotifyAssignmentForUser:
    TITLE = "*Assignment Reminder*\n\n"
    NEW_ASSIGNMENT_TITLE = "*New Assignment*\n\n"
    COURSE_SUMMARY = ":point_right: Summary: *"
    START_DATE = ":point_right: Start date: *"
    DUE_DATE = ":point_right: Due date: *"
    STATUS = ":point_right: Status: *"
