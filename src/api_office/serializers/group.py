from api_office.models import Group
from api_office.services import GroupService
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

    def validate(self, attrs):
        parent_group = attrs.get("parent_group", None)
        instance_id = None
        if self.instance:
            instance_id = self.instance.id
        if (
            not parent_group
            and Group.objects.filter(parent_group=None).exclude(id=instance_id).exists()
        ):
            raise ValidationError(
                {
                    "details": "Existed another root group, please input your parent group id"
                }
            )
        return attrs

    def update(self, instance, validated_data):
        validated_data = GroupService.update(instance, validated_data)
        return super().update(instance, validated_data)
