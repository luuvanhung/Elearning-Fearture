from api_user.models.profile import Profile
from api_workday.models.remain_leave import RemainLeave
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "name", "join_date", "office"]


class RemainLeaveSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = RemainLeave
        fields = "__all__"
        read_only_fields = ["profile"]
