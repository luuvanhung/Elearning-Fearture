from api_wfh.models.wfh_date import WfhDate
from api_wfh.models.wfh_request import WfhRequest
from rest_framework import serializers


class WfhRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WfhRequest
        fields = ["id", "reason"]


class WfhDateForCalendarSerializer(serializers.ModelSerializer):
    wfh_request = WfhRequestSerializer(read_only=True)

    class Meta:
        model = WfhDate
        fields = ["id", "wfh_request", "date"]
