from api_probation.models import EvaluationTemplate
from api_probation.serializers.evaluation_template_competence import (
    EvaluationTemplateCompetenceSerializer,
)
from api_probation.serializers.evaluation_template_overall_comment import (
    EvaluationTemplateOverallCommentSerializer,
)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class EvaluationTemplateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(allow_null=True, required=False)
    competencies = EvaluationTemplateCompetenceSerializer(many=True, required=False)
    overall_comments = EvaluationTemplateOverallCommentSerializer(
        many=True, required=False
    )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["name_type"] = instance.type.type_name if instance.type else None
        return ret

    class Meta:
        model = EvaluationTemplate
        fields = [
            "id",
            "name",
            "office",
            "type",
            "status",
            "created_at",
            "updated_at",
            "competencies",
            "overall_comments",
        ]

    def validate(self, attrs):
        if EvaluationTemplate.objects.filter(name=attrs.get("name", "")).exists():
            raise ValidationError(
                {"error": "This Evaluation Template name already existed"}
            )
        return attrs

    def create(self, validated_data):
        instance = EvaluationTemplate.objects.create(
            office=validated_data.get("office"),
            name=validated_data.get("name"),
            status=True,
        )
        return instance


class CreateEvaluationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationTemplate
        fields = "__all__"
