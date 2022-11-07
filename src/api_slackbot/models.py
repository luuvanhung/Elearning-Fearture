import uuid

from api_base.models.timestamped import TimeStampedModel
from api_user.models.profile import Profile
from api_workday.models.leave_type import LeaveType
from common.constants.workday_constants.date import Workday
from common.constants.workday_constants.leave_type import Leave
from django.db import models


class TempLeaveRequest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    leave_type = models.ForeignKey(
        LeaveType, default=None, on_delete=models.SET_NULL, null=True
    )
    from_date = models.CharField(max_length=255, null=True)
    from_time = models.CharField(
        max_length=255,
        choices=[
            (Workday.DEFAULT_START_HOUR, Workday.DEFAULT_START_HOUR),
            (
                Workday.DEFAULT_START_HOUR_AFTERNOON,
                Workday.DEFAULT_START_HOUR_AFTERNOON,
            ),
        ],
        default=Workday.DEFAULT_START_HOUR,
    )
    to_date = models.CharField(max_length=255, null=True)
    to_time = models.CharField(
        max_length=255,
        choices=[
            (Workday.DEFAULT_END_HOUR_MORNING, Workday.DEFAULT_END_HOUR_MORNING),
            (Workday.DEFAULT_END_HOUR, Workday.DEFAULT_END_HOUR),
        ],
        default=Workday.DEFAULT_END_HOUR,
    )
    reason = models.TextField(null=False, default=Leave.DEFAULT_LEAVE_REASON)
    lunch_status = models.BooleanField(default=False)
    """
    We have this is_have_lunch_flag field due to the slack's request flow, here is the case:
        -If a full-day leave request was created, the is_have_lunch automatically updated to False
            despite the user has CHECKED THE "HAVE-LUNCH" CHECKBOX OPTION or not (ASSUME THAT THEY CHECKED).
        -Now user may change the time to half-day leave and the "have-lunch" checkbox was checked as we assumed above,
            but the is_have_lunch still equal to False in temp_leave_request_table.

    That's why we create this field to check if user has checked the "have-lunch" checkbox for full-day leave request,
    then change to half-day leave request or not
    """

    # At this moment, we may temporarily disable this field as client's requirements
    # that users still can have lunch no matter full day leave or not

    full_day_leave_lunch_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "temp_leave_request"
