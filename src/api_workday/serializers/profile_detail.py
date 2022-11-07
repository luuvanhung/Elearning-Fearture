from api_user.models.profile import Profile
from api_workday.models.remain_leave import RemainLeave
from rest_framework import serializers


class RemainLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemainLeave
        fields = ["id", "year", "annual_leave", "current_days_off"]


class ProfileDetailSerizlizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    def get_user(self, obj):
        return {"id": obj.user.id, "email": obj.user.email}

    class Meta:
        model = Profile
        fields = ["id", "name", "user"]
