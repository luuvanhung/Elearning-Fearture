from common.constants.base_const import Const

__all__ = ["Workday"]


class Workday(Const):
    LEAVE = "Leave"
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    FULL = "All day"
    WFH = "Work from home"

    MORNING_SHIFT_TIME = "08:00-12:00"
    AFTERNOON_SHIFT_TIME = "13:30-17:30"

    DEFAULT_START_HOUR = "08:00"
    DEFAULT_END_HOUR = "17:30"
    DEFAULT_END_HOUR_MORNING = "12:00"
    DEFAULT_START_HOUR_AFTERNOON = "13:30"

    STATUS_ACCEPTED = "Accepted"
    STATUS_PASSED = "Passed"
    STATUS_PENDING = "Pending"
    STATUS_REJECTED = "Rejected"
    STATUS_CANCELING = "Canceling"
    STATUS_CANCELED = "Canceled"
    STATUS_FORWARDED = "Forwarded"
    STATUS_APPROVED = "Approved"

    FIRST_MONTH = 0
    LAST_MONTH = 12

    FIRST_DAY = 0
    LAST_DAY = 31

    STT_NUM_NOT_ENOUGH = "The number of days off is not enough"

    HALF_DAY_TIME = 4
    END_HOUR_MORNING = 12
    RATIO_ACCEPT = 0.6

    MAX_REMAIN_DAY = 32
    MAX_ANNUAL_LEAVE = 20
    DEFAULT_ANNUAL_DAY = 12

    HALF_YEAR = 6
    MONTHS_OF_YEAR = 12
    EXPIRED_MONTH = 18
