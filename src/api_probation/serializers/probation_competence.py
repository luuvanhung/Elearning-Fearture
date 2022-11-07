from api_probation.models import ProbationCompetence
from api_probation.serializers.evaluation_template_competence_assessor_role import (
    EvaluationTemplateCompetenceAssessorRoleSerializer,
)
from api_probation.services.probation_competence import ProbationCompetenceService
from api_user.serializers import UserSerializer
from rest_framework import serializers


class CreateListProbationCompetenceSerializer(serializers.ListSerializer):
    def create(self, probation_competencies):
        probation_id = self.context.get("probation_id") or None
        employee_id = self.context.get("employee_id") or None
        return ProbationCompetenceService.create(
            probation_competencies, probation_id, employee_id
        )

    def update(self, competencies, new_competencies):
        probation_line_manager = self.context.get("probation_line_manager") or None
        return ProbationCompetenceService.update(
            competencies, new_competencies, probation_line_manager
        )

    class Meta:
        model = ProbationCompetence
        fields = "__all__"


class ProbationCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationCompetence
        list_serializer_class = CreateListProbationCompetenceSerializer
        exclude = ["probation", "employee"]


class UpdateProbationCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationCompetence
        list_serializer_class = CreateListProbationCompetenceSerializer
        exclude = ["probation", "employee", "assessor"]


class ListProbationCompetenceSerializer(serializers.ModelSerializer):
    assessor = UserSerializer(many=False, read_only=True)
    assessor_roles = EvaluationTemplateCompetenceAssessorRoleSerializer(
        many=True, required=False
    )

    class Meta:
        model = ProbationCompetence
        depth = 1
        include = ["assessor_roles"]
        exclude = ["created_at", "updated_at", "probation", "employee"]
