from api_workday.models.request_off import RequestOff
from api_workday.serializers.date_off import DateOffSerializer
from rest_framework import serializers


class RequestOffSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    date_off = DateOffSerializer(many=True, read_only=True)
    leave_type = serializers.SerializerMethodField("get_type")
    profile = serializers.SerializerMethodField("get_profile")
    request_detail = serializers.StringRelatedField(
        many=True, read_only=True
    )

    @staticmethod
    def get_type(obj):
        return {
            "id": obj.leave_type.id,
            "name": obj.leave_type.name,
            "is_count": obj.leave_type.is_count,
        }

    @staticmethod
    def get_profile(obj):
        return {"id": obj.profile.id, "name": obj.profile.name, "email": obj.profile.user.email}

    class Meta:
        model = RequestOff
        fields = "__all__"
        read_only_fields = ["leave_type", "profile"]
