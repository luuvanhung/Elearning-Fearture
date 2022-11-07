from api_probation.models import EvaluationTemplateCompetenceAssessorRole
from rest_framework import serializers


class EvaluationTemplateCompetenceAssessorRoleSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = EvaluationTemplateCompetenceAssessorRole
        fields = ["id", "assessor_role", "evaluation_competence"]
