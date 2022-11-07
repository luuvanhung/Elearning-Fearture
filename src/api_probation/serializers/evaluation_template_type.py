from api_probation.models.evaluation_template_type import EvaluationTemplateType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class EvaluationTemplateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationTemplateType
        fields = "__all__"

    def validate(self, attrs):
        if EvaluationTemplateType.objects.filter(
            type_name=attrs.get("type_name", "")
        ).exists():
            raise ValidationError(
                {"error": "This Evaluation Template type already existed"}
            )
        return attrs
