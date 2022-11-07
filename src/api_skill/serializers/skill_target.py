from api_skill.models import SkillTarget
from api_skill.services import SkillTargetService
from api_user.serializers import UserVoteSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class SkillTargetSerializer(serializers.ModelSerializer):
    set_by_user = UserVoteSerializer(required=False)

    class Meta:
        model = SkillTarget
        fields = ["id", "target_user", "skill_definition", "set_by_user"]

    def validate(self, attrs):
        request = self.context.get("request")
        access_user = request.user
        attrs["set_by_user"] = access_user

        return attrs

    def create(self, validated_data):
        error_message = SkillTargetService.is_valid(validated_data)
        if error_message:
            raise ValidationError({"details": error_message})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        error_message = SkillTargetService.is_valid(validated_data, instance.id)
        if error_message:
            raise ValidationError({"details": error_message})

        return super().update(instance, validated_data)
