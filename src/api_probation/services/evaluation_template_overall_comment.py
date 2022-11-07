from api_base.services import BaseService
from api_probation.models import (
    EvaluationTemplateOverallComment,
    EvaluationTemplateOverallCommentAssessorRole,
)


class EvaluationTemplateOverallCommentService(BaseService):
    @classmethod
    def create_list_overall_comment(cls, overall_comments, evaluation_template):
        objs = (
            EvaluationTemplateOverallComment(
                term=overall_comment.get("term"),
                evaluation_template_id=evaluation_template.get("id"),
            )
            for overall_comment in overall_comments
        )
        return objs

    @classmethod
    def get_list_update(cls, overall_comments):
        overall_comment_objs = EvaluationTemplateOverallComment.objects.filter(
            id__in=[overall_comment["id"] for overall_comment in overall_comments]
        )
        for (_idx, overall_comment) in enumerate(overall_comment_objs):
            overall_comment.term = overall_comments[_idx].get("term")
        return overall_comment_objs

    @classmethod
    def handle_data_update(cls, overall_comments, evaluation_template_id):
        overall_comment_update = []
        overall_comment_assessor_update = []
        overall_comment_create = []  # to create( no id competencies)
        overall_comment_assessor_create = []  # to create( has id overall_comment)
        overall_comment_delete = [
            str(overall_comment.id)
            for overall_comment in EvaluationTemplateOverallComment.objects.filter(
                evaluation_template_id=evaluation_template_id
            )
        ]
        overall_comment_assessor_delete = [
            str(assessor.id)
            for assessor in EvaluationTemplateOverallCommentAssessorRole.objects.filter(
                overall_comment_id__in=overall_comment_delete
            )
        ]

        for overall_comment in overall_comments:
            if "id" in overall_comment:
                overall_comment_delete.remove(overall_comment.get("id"))
                for (_idx, assessor) in enumerate(
                    overall_comment.get("assessor_roles")
                ):

                    if "id" not in assessor:
                        assessor.update({"overall_comment": overall_comment.get("id")})
                        overall_comment_assessor_create.append(
                            overall_comment.get("assessor_roles")[_idx]
                        )
                    else:
                        overall_comment_assessor_delete.remove(assessor.get("id"))
                        overall_comment_assessor_update.append(assessor)
                overall_comment.pop("assessor_roles")
                overall_comment_update.append(overall_comment)
            else:
                overall_comment_create.append(overall_comment)

        return {
            "overall_comment_update": overall_comment_update,
            "overall_comment_assessor_update": overall_comment_assessor_update,
            "overall_comment_create": overall_comment_create,
            "overall_comment_assessor_create": overall_comment_assessor_create,
            "overall_comment_delete": overall_comment_delete,
            "overall_comment_assessor_delete": overall_comment_assessor_delete,
        }
