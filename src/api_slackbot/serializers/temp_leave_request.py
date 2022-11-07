from api_slackbot.models import TempLeaveRequest
from common.constants.workday_constants.date import Workday
from rest_framework import serializers


class TempLeaveRequestSerializer(serializers.ModelSerializer):
    leave_type = serializers.SerializerMethodField("get_type")
    profile = serializers.SerializerMethodField("get_profile")
    from_date = serializers.CharField(max_length=255, allow_null=True)
    from_time = serializers.ChoiceField(
        [
            (Workday.DEFAULT_START_HOUR, Workday.DEFAULT_START_HOUR),
            (
                Workday.DEFAULT_START_HOUR_AFTERNOON,
                Workday.DEFAULT_START_HOUR_AFTERNOON,
            ),
        ]
    )
    to_date = serializers.CharField(max_length=255, allow_null=True)
    to_time = serializers.SerializerMethodField(
        [
            (Workday.DEFAULT_END_HOUR_MORNING, Workday.DEFAULT_END_HOUR_MORNING),
            (Workday.DEFAULT_END_HOUR, Workday.DEFAULT_END_HOUR),
        ]
    )

    class Meta:
        model = TempLeaveRequest
        fields = "__all__"
