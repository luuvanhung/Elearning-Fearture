from api_workday.models.date_off import DateOff
from api_workday.models.leave_type import LeaveType
from api_workday.models.request_off import RequestOff
from rest_framework import serializers


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class RequestOffSerializer(serializers.ModelSerializer):
    leave_type = LeaveTypeSerializer(read_only=True)

    class Meta:
        model = RequestOff
        fields = ["id", "leave_type", "reason"]


class DateOffForCalendarSerializer(serializers.ModelSerializer):
    request_off = RequestOffSerializer(read_only=True)

    class Meta:
        model = DateOff
        fields = ["id", "request_off", "date", "type", "lunch"]
