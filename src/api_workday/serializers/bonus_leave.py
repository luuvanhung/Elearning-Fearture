from api_workday.models import BonusLeave
from api_workday.serializers import BonusTypeSerializer
from rest_framework import serializers


class BonusLeaveSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    profile = serializers.SerializerMethodField(read_only=True)
    bonus_type = BonusTypeSerializer()

    class Meta:
        model = BonusLeave
        fields = [
            'id',
            'created_at',
            'reason',
            'bonus_days',
            'bonus_type',
            'profile'
        ]

    def get_profile(self, obj):
        from api_user.serializers import ProfileInlineSerializers
        return ProfileInlineSerializers(obj.profile).data


class CUBonusLeaveSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        from api_workday.services import BonusLeaveService
        bonus_leave = BonusLeave.objects.create(**validated_data)
        BonusLeaveService.add_expired_date_bonus_leave(validated_data.get("profile"), bonus_leave.id)
        return bonus_leave

    class Meta:
        model = BonusLeave
        fields = '__all__'
