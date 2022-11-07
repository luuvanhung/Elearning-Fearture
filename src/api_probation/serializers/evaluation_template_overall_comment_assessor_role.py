from api_probation.models import EvaluationTemplateOverallCommentAssessorRole
from api_probation.services.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRoleService,
)
from api_user.models.profile import Profile
from rest_framework import serializers


class EvaluationTemplateOverallCommentAssessorRoleSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = EvaluationTemplateOverallCommentAssessorRole
        fields = ["id", "overall_comment_role", "overall_comment"]


class EvaluationTemplateOverallCommentAssessorRoleDepthSerializer(
    serializers.ModelSerializer
):
    def to_representation(self, instance):
        probation_line_manager_id = (
            self.context.get("probation_line_manager_id") or None
        )
        employee_id = self.context.get("employee_id") or None

        ret = super().to_representation(instance)
        if instance.overall_comment:
            ret["evaluation_template_overall_comment"] = instance.overall_comment.id
        if instance.id:
            ret["evaluation_template_overall_comment_assessor_role"] = instance.id
        assessor = (
            EvaluationTemplateOverallCommentAssessorRoleService.get_assessor_by_role(
                instance.overall_comment_role, employee_id, probation_line_manager_id
            )
        )
        assessor_name = None
        if assessor:
            assessor_name = Profile.objects.filter(user_id=assessor).first().name
        ret.update(score=0, comments="", assessor=assessor, assessor_name=assessor_name)
        return ret

    class Meta:
        model = EvaluationTemplateOverallCommentAssessorRole
        fields = ["id", "overall_comment_role", "overall_comment"]
        depth = 1
