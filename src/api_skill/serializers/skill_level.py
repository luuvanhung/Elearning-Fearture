from api_skill.models import SkillLevel
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class SkillLevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    weight = serializers.IntegerField()

    class Meta:
        model = SkillLevel
        fields = ["id", "name", "weight"]

    def create(self, validated_data):
        name = validated_data.get("name")
        weight = validated_data.get("weight")

        if SkillLevel.objects.filter(name=name).exists():
            raise ValidationError({"detail": "This level name already existed"})
        if SkillLevel.objects.filter(weight=weight).exists():
            raise ValidationError({"detail": "This weight already existed"})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name", "").strip()
        weight = validated_data.get("weight", 0)

        if not name:
            raise ValidationError({"detail": "name is empty"})
        if not weight:
            raise ValidationError({"detail": "weight is empty"})

        if SkillLevel.objects.filter(name=name).exclude(id=instance.id).exists():
            raise ValidationError({"detail": "This level name already existed"})
        if SkillLevel.objects.filter(weight=weight).exclude(id=instance.id).exists():
            raise ValidationError({"detail": "This weight already existed"})

        return super().update(instance, validated_data)


class FullSkillLevelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    weight = serializers.IntegerField()

    class Meta:
        model = SkillLevel
        fields = ["id", "name", "weight"]


class LevelSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        max_length=50, validators=[UniqueValidator(queryset=SkillLevel.objects.all())]
    )

    class Meta:
        model = SkillLevel
        fields = ["id", "name", "weight"]
