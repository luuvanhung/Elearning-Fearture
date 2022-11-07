from api_skill.models import SkillVote
from api_skill.serializers import SkillDefinitionSerializer
from api_skill.services import SkillVoteService
from api_user.serializers import UserVoteSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ListSkillVoteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    voted_user = UserVoteSerializer()
    skill_definition = SkillDefinitionSerializer()

    class Meta:
        model = SkillVote
        fields = ["id", "voted_user", "skill_definition"]


class ListCurrentSkillSerializer(serializers.ModelSerializer):
    voter = UserVoteSerializer()
    # skill_definition =

    class Meta:
        model = SkillVote
        fields = ["id", "voter", "skill_definition"]


class CreateSkillVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillVote
        fields = ["id", "voted_user", "skill_definition"]

    def validate(self, attrs):
        request = self.context.get("request")
        voter = request.user
        attrs["voter"] = voter

        return attrs

    def create(self, validated_data):
        error_message = SkillVoteService.is_valid_vote(validated_data)
        if error_message:
            raise ValidationError({"detail": error_message})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        error_message = SkillVoteService.is_valid_vote(validated_data, instance.id)
        if error_message:
            raise ValidationError({"detail": error_message})
        return super().update(instance, validated_data)
