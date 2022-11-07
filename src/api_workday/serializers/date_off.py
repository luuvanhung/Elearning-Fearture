from api_workday.models.date_off import DateOff
from rest_framework import serializers


class DateOffSerializer(serializers.ModelSerializer):
    request_off = serializers.SerializerMethodField("get_request")

    @staticmethod
    def get_request(obj):
        return {
            "id": obj.request_off.id,
            "type_name": obj.request_off.leave_type.name,
        }

    class Meta:
        model = DateOff
        fields = "__all__"
