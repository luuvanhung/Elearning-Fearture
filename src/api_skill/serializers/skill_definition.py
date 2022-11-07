from api_skill.models import SkillDefinition, SkillLevel
from api_skill.serializers import FullSkillLevelSerializer, FullSkillSerializer
from api_skill.services import SkillDefinitionService
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SkillDefinitionSerializer(serializers.ModelSerializer):
    skill = FullSkillSerializer()
    level = FullSkillLevelSerializer()
    requirements = serializers.CharField(required=False)

    class Meta:
        model = SkillDefinition
        fields = ["id", "skill", "level", "requirements"]

    def validate(self, attrs):
        if not SkillLevel.objects.filter(
            id=attrs.get("level", {}).get("id", None)
        ).exists():
            raise ValidationError({"detail": "This level id does not exist"})

        return attrs

    def create(self, validated_data):
        validated_data = SkillDefinitionService.create(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = SkillDefinitionService.update(instance, validated_data)
        return super().update(instance, validated_data)
