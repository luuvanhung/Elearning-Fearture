from api_workday.models.leave_type_group import LeaveTypeGroup
from rest_framework import serializers


class LeaveTypeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveTypeGroup
        exclude = ["created_at", "updated_at"]

    def create(self, validated_data):
        if LeaveTypeGroup.objects.filter(name=validated_data["name"]).exists():
            return None
        return LeaveTypeGroup.objects.create(**validated_data)
