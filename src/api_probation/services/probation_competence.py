from api_base.services import BaseService
from api_probation.models import ProbationCompetence


class ProbationCompetenceService(BaseService):
    @classmethod
    def create(cls, probation_competencies, probation_id, employee_id):
        if probation_id and employee_id:
            list_obj = [
                (
                    ProbationCompetence(
                        **item, probation_id=probation_id, employee_id=employee_id
                    )
                )
                for item in probation_competencies
            ]
        else:
            list_obj = [
                (ProbationCompetence(**item)) for item in probation_competencies
            ]
        return ProbationCompetence.objects.bulk_create(list_obj)

    @classmethod
    def update(cls, competencies, validated_competencies, probation_line_manager):
        competence_objs = ProbationCompetence.objects.filter(
            id__in=[competence.get("id") for competence in competencies]
        )

        for _idx, competence in enumerate(competence_objs):
            competence.score = competencies[_idx].get("score")
            competence.comments = competencies[_idx].get("comments")
            competence.assessor_id = (
                competencies[_idx].get("assessor_id")
                if competencies[_idx].get("competence_role") != "Line Manager"
                else probation_line_manager
            )

        ProbationCompetence.objects.bulk_update(
            competence_objs, ["comments", "score", "assessor_id"]
        )
        return competence_objs
