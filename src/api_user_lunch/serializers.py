from api_user.models import Profile
from rest_framework import serializers

from .models import UserLunch


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Profile User Lunch"
        model = Profile
        fields = "__all__"


class UserLunchSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = UserLunch
        fields = "__all__"


class CreateUserLunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLunch
        fields = "__all__"
