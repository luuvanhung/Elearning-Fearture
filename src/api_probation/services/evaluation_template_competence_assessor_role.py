from api_base.services import BaseService
from api_probation.models import EvaluationTemplateCompetenceAssessorRole
from common.constants.probation_constant import AssessorRoleConstant


class EvaluationTemplateCompetenceAssessorRoleService(BaseService):
    @classmethod
    def create_list_competence_assessor_role(cls, competencies, competence_objs):
        assessors_data = []
        for _idx, competency in enumerate(competencies):
            assessors = competency.get("assessor_roles")
            for assessor in assessors:
                item = {"evaluation_competence": competence_objs[_idx]}
                item.update({"assessor_role": assessor["assessor_role"]})
                assessors_data.append(item)
        assessor_objs = (
            EvaluationTemplateCompetenceAssessorRole(**assessor)
            for assessor in assessors_data
        )
        return assessor_objs

    @classmethod
    def get_list_update(cls, assessors):
        assessor_objs = EvaluationTemplateCompetenceAssessorRole.objects.filter(
            id__in=[assessor["id"] for assessor in assessors]
        ).order_by("id")
        assessor_sort = sorted(assessors, key=lambda item: item["id"])
        for (_idx, assessor) in enumerate(assessor_objs):
            assessor.assessor_role = assessor_sort[_idx].get("assessor_role")
        return assessor_objs

    @classmethod
    def get_list_create(cls, competencies):
        assessor_objs = (
            EvaluationTemplateCompetenceAssessorRole(
                evaluation_competence_id=assessor["evaluation_competence"],
                assessor_role=assessor["assessor_role"],
            )
            for assessor in competencies
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
