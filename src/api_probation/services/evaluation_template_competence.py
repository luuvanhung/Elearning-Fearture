from api_base.services import BaseService
from api_probation.models import (
    EvaluationTemplateCompetence,
    EvaluationTemplateCompetenceAssessorRole,
)


class EvaluationTemplateCompetenceService(BaseService):
    @classmethod
    def create_list_competence(cls, competencies, evaluation_template):
        objs = (
            EvaluationTemplateCompetence(
                competence=competence.get("competence"),
                evaluation_template_id=evaluation_template.get("id"),
            )
            for competence in competencies
        )
        return objs

    @classmethod
    def get_list_update(cls, competencies):
        competence_objs = EvaluationTemplateCompetence.objects.filter(
            id__in=[competence["id"] for competence in competencies]
        )
        for (_idx, competence) in enumerate(competence_objs):
            competence.competence = competencies[_idx].get("competence")
        return competence_objs

    @classmethod
    def handle_data_update(cls, competencies, evaluation_template_id):
        competencies_update = []
        competencies_assessor_update = []
        competencies_create = []  # to create( no id competencies)
        competencies_assessor_create = []  # to create( has id competencies)
        competencies_delete = [
            str(competence.id)
            for competence in EvaluationTemplateCompetence.objects.filter(
                evaluation_template_id=evaluation_template_id
            )
        ]
        competencies_assessor_delete = [
            str(assessor.id)
            for assessor in EvaluationTemplateCompetenceAssessorRole.objects.filter(
                evaluation_competence_id__in=competencies_delete
            )
        ]

        for competence in competencies:
            if "id" in competence:
                competencies_delete.remove(competence.get("id"))
                for (_idx, assessor) in enumerate(competence.get("assessor_roles")):
                    if "id" not in assessor:
                        assessor.update({"evaluation_competence": competence.get("id")})
                        competencies_assessor_create.append(
                            competence.get("assessor_roles")[_idx]
                        )
                    else:
                        competencies_assessor_delete.remove(assessor.get("id"))
                        competencies_assessor_update.append(assessor)
                competence.pop("assessor_roles")
                competencies_update.append(competence)
            else:
                competencies_create.append(competence)
        return {
            "competencies_update": competencies_update,
            "competencies_assessor_update": competencies_assessor_update,
            "competencies_create": competencies_create,
            "competencies_assessor_create": competencies_assessor_create,
            "competencies_delete": competencies_delete,
            "competencies_assessor_delete": competencies_assessor_delete,
        }
