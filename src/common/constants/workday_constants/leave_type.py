from common.constants.base_const import Const

__all__ = ["LeaveTypeConstant"]


class Leave:
    DEFAULT_LEAVE_REASON = "Personal issues"
    DEFAULT_LEAVE_TYPE = "Annual Leave"
    COUNT_DAYS_LEFT = 1


class LeaveTypeConstant(Const):
    """
    Leave type constants
    """
    ANNUAL_LEAVE = "Annual Leave"
    THE_EMPLOYEES_MARRIAGE = "The Employees Marriage"
    THE_EMPLOYEES_MARRIAGE_CHILDREN = "Marriage of Employees' children"
    FUNERAL_LEAVE = "Funeral Leave"
    PATERNITY_LEAVE = "Paternity Leave"
    MATERNITY_LEAVE = "Maternity Leave"
    SICK_LEAVE = "Sick Leave"
    OTHERS = "Others"
