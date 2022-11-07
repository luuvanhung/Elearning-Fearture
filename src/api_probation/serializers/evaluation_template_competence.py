from api_probation.models import EvaluationTemplateCompetence
from api_probation.serializers.evaluation_template_competence_assessor_role import (
    EvaluationTemplateCompetenceAssessorRoleSerializer,
)
from rest_framework import serializers


class EvaluationTemplateCompetenceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    assessor_roles = EvaluationTemplateCompetenceAssessorRoleSerializer(
        many=True, required=False
    )

    class Meta:
        model = EvaluationTemplateCompetence
        fields = ["id", "competence", "assessor_roles"]
