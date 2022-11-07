from api_probation.models.probation_overall_comment import ProbationOverallComment
from api_probation.serializers.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRoleSerializer,
)
from api_probation.services.probation_overall_comment import (
    ProbationOverallCommentService,
)
from api_user.serializers import UserSerializer
from rest_framework import serializers


class CreateListProbationOverallCommentSerializer(serializers.ListSerializer):
    def create(self, probation_overall_comments):
        probation_id = self.context.get("probation_id") or None
        employee_id = self.context.get("employee_id") or None
        return ProbationOverallCommentService.create(
            probation_overall_comments, probation_id, employee_id
        )

    def update(self, overalls, new_overalls):
        probation_line_manager = self.context.get("probation_line_manager") or None
        return ProbationOverallCommentService.update(
            overalls, new_overalls, probation_line_manager
        )

    class Meta:
        model = ProbationOverallComment
        fields = "__all__"


class ProbationOverallCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationOverallComment
        list_serializer_class = CreateListProbationOverallCommentSerializer
        exclude = ["probation", "employee"]


class UpdateProbationOverallCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationOverallComment
        list_serializer_class = CreateListProbationOverallCommentSerializer
        exclude = [
            "probation",
            "employee",
            "evaluation_template_overall_comment",
            "evaluation_template_overall_comment_assessor_role",
            "assessor",
        ]


class ListProbationOverallCommentSerializer(serializers.ModelSerializer):
    assessor = UserSerializer(many=False, read_only=True)
    assessor_roles = EvaluationTemplateOverallCommentAssessorRoleSerializer(
        many=True, required=False
    )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["assessor_id"] = instance.assessor.id if instance.assessor else None
        return ret

    class Meta:
        model = ProbationOverallComment
        depth = 1
        include = ["assessor_roles"]
        exclude = ["created_at", "updated_at", "probation", "employee"]
