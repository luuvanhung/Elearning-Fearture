from api_probation.models import EvaluationTemplateOverallComment
from api_probation.serializers.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRoleSerializer,
)
from rest_framework import serializers


class EvaluationTemplateOverallCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    assessor_roles = EvaluationTemplateOverallCommentAssessorRoleSerializer(
        many=True, required=False
    )

    class Meta:
        model = EvaluationTemplateOverallComment
        fields = ["id", "term", "created_at", "updated_at", "assessor_roles"]
