from api_base.services import BaseService
from api_probation.models import ProbationOverallComment


class ProbationOverallCommentService(BaseService):
    @classmethod
    def create(cls, probation_overall_comments, probation_id, employee_id):
        if probation_id and employee_id:
            list_obj = [
                (
                    ProbationOverallComment(
                        **item, probation_id=probation_id, employee_id=employee_id
                    )
                )
                for item in probation_overall_comments
            ]
        else:
            list_obj = [
                (ProbationOverallComment(**item)) for item in probation_overall_comments
            ]
        return ProbationOverallComment.objects.bulk_create(list_obj)

    @classmethod
    def update(cls, overalls, validated_overalls, probation_line_manager):
        overalls_objs = ProbationOverallComment.objects.filter(
            id__in=[overall.get("id") for overall in overalls]
        )

        for _idx, overall in enumerate(overalls_objs):
            overall.score = overalls[_idx].get("score")
            overall.comments = overalls[_idx].get("comments")
            overall.assessor_id = (
                overalls[_idx].get("assessor_id")
                if overalls[_idx]
                .get("evaluation_template_overall_comment_assessor_role")
                .get("overall_comment_role")
                != "Line Manager"
                else probation_line_manager
            )

        ProbationOverallComment.objects.bulk_update(
            overalls_objs, ["comments", "score", "assessor_id"]
        )
        return overalls_objs
