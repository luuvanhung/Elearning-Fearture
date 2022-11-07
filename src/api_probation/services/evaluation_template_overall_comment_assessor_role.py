from api_base.services import BaseService
from api_probation.models import EvaluationTemplateOverallCommentAssessorRole
from common.constants.probation_constant import AssessorRoleConstant


class EvaluationTemplateOverallCommentAssessorRoleService(BaseService):
    @classmethod
    def create_list_overall_comment_assessor_role(
        cls, overall_comments, overall_comment_objs
    ):
        assessors_data = []
        for _idx, overall_comment in enumerate(overall_comments):
            assessors = overall_comment.get("assessor_roles")
            for assessor in assessors:
                item = {"overall_comment": overall_comment_objs[_idx]}
                item.update({"overall_comment_role": assessor["overall_comment_role"]})
                assessors_data.append(item)
        assessor_objs = (
            EvaluationTemplateOverallCommentAssessorRole(**assessor)
            for assessor in assessors_data
        )
        return assessor_objs

    @classmethod
    def get_list_update(cls, assessors):
        assessor_objs = EvaluationTemplateOverallCommentAssessorRole.objects.filter(
            id__in=[overall_comment["id"] for overall_comment in assessors]
        )
        for (_idx, overall_comment) in enumerate(assessor_objs):
            overall_comment.overall_comment_role = assessors[_idx].get(
                "overall_comment_role"
            )
        return assessor_objs

    @classmethod
    def get_list_create(cls, assessors):
        assessor_objs = (
            EvaluationTemplateOverallCommentAssessorRole(
                overall_comment_id=assessor["overall_comment"],
                overall_comment_role=assessor["overall_comment_role"],
            )
            for assessor in assessors
        )
        return assessor_objs

    @classmethod
    def get_assessor_by_role(cls, role, employee_id, probation_line_manager_id):
        if role:
            if AssessorRoleConstant.SELF_ROLE in role:
                return employee_id
            elif AssessorRoleConstant.LINE_MANAGER_ROLE in role:
                return probation_line_manager_id
            else:
                return None
