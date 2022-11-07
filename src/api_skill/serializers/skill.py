from api_skill.models import Skill
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Skill.objects.all())],
        allow_blank=False,
        allow_null=False,
    )

    class Meta:
        model = Skill
        fields = ["id", "name"]


class FullSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

    class Meta:
        model = Skill
        fields = ["id", "name"]
