from functools import reduce

from api_base.views import BaseViewSet
from api_probation.models import (
    EvaluationTemplate,
    EvaluationTemplateCompetence,
    EvaluationTemplateCompetenceAssessorRole,
    EvaluationTemplateOverallComment,
    EvaluationTemplateOverallCommentAssessorRole,
)
from api_probation.serializers import (
    EvaluationTemplateCompetenceSerializer,
    EvaluationTemplateSerializer,
)
from api_probation.serializers.evaluation_template import (
    CreateEvaluationTemplateSerializer,
)
from api_probation.serializers.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRoleDepthSerializer,
)
from api_probation.services.evaluation_template_competence import (
    EvaluationTemplateCompetenceService,
)
from api_probation.services.evaluation_template_competence_assessor_role import (
    EvaluationTemplateCompetenceAssessorRoleService,
)
from api_probation.services.evaluation_template_overall_comment import (
    EvaluationTemplateOverallCommentService,
)
from api_probation.services.evaluation_template_overall_comment_assessor_role import (
    EvaluationTemplateOverallCommentAssessorRoleService,
)
from api_user.models.profile import Profile
from common.constants.api_constants import HttpMethod
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class EvaluationTemplateViewSet(BaseViewSet):
    queryset = EvaluationTemplate.objects.all().order_by("-updated_at")
    serializer_class = EvaluationTemplateSerializer
    required_alternate_scopes = {
        "create": [["evaluation_template:create"]],
        "retrieve": [["evaluation_template:view"]],
        "update": [["evaluation_template:edit"]],
        "destroy": [["evaluation_template:destroy"]],
        "list": [["evaluation_template:view"]],
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        with transaction.atomic():
            evaluation_template = CreateEvaluationTemplateSerializer(data=data)
            if evaluation_template.is_valid(raise_exception=True):
                evaluation_template.save()
            competencies = EvaluationTemplateCompetenceService.create_list_competence(
                data.get("competencies"), evaluation_template.data
            )
            competence_objs = EvaluationTemplateCompetence.objects.bulk_create(
                competencies
            )
            assessors = EvaluationTemplateCompetenceAssessorRoleService.create_list_competence_assessor_role(
                data.get("competencies"), competence_objs
            )
            EvaluationTemplateCompetenceAssessorRole.objects.bulk_create(assessors)

            overall_comments = (
                EvaluationTemplateOverallCommentService.create_list_overall_comment(
                    data.get("overall_comments"), evaluation_template.data
                )
            )
            overall_comment_objs = EvaluationTemplateOverallComment.objects.bulk_create(
                overall_comments
            )

            assessors = EvaluationTemplateOverallCommentAssessorRoleService.create_list_overall_comment_assessor_role(
                data.get("overall_comments"), overall_comment_objs
            )
            EvaluationTemplateOverallCommentAssessorRole.objects.bulk_create(assessors)

        return Response(
            {"success": "Evaluation Template is created success"},
            status=status.HTTP_201_CREATED,
        )

    @action(methods=[HttpMethod.GET], detail=False)
    def get_competence_assessor_role(self, request, *args, **kwargs):
        try:
            evaluation_template_id = self.request.query_params.get(
                "evaluation_template_id", None
            )
            query_set = (
                EvaluationTemplateCompetenceAssessorRole.objects.select_related(
                    "evaluation_competence"
                )
                .filter(
                    evaluation_competence__evaluation_template=evaluation_template_id
                )
                .order_by("-assessor_role")
                .values_list("assessor_role", flat=True)
                .distinct()
            )
            return Response(query_set, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_overall_assessor_role(self, request, *args, **kwargs):
        try:
            evaluation_template_id = self.request.query_params.get(
                "evaluation_template_id", None
            )
            query_set = (
                EvaluationTemplateOverallCommentAssessorRole.objects.filter(
                    overall_comment__evaluation_template=evaluation_template_id
                )
                .order_by("-overall_comment_role")
                .values_list("overall_comment_role", flat=True)
            )
            return Response(query_set, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_evaluation_competence_and_role(self, request, *args, **kwargs):
        try:
            evaluation_template_id = self.request.query_params.get(
                "evaluation_template_id", None
            )
            employee_id = self.request.query_params.get("employee_id", None)
            probation_line_manager_id = self.request.query_params.get(
                "probation_line_manager_id", None
            )
            competence_queryset = (
                EvaluationTemplateCompetence.objects.select_related(
                    "evaluation_template"
                )
                .filter(evaluation_template=evaluation_template_id)
                .order_by("-created_at")
            )
            competences = []
            combine_all_role = {}
            for competence in competence_queryset:
                item = EvaluationTemplateCompetenceSerializer(competence).data

                def transform_data(obj, element):
                    change_key = element.get("assessor_role")
                    assessor = EvaluationTemplateCompetenceAssessorRoleService.get_assessor_by_role(
                        change_key, employee_id, probation_line_manager_id
                    )
                    assessor_name = None
                    if assessor:
                        assessor_name = (
                            Profile.objects.filter(user_id=assessor).first().name
                        )
                    if change_key:
                        combine_all_role.update({change_key: {"assessor": assessor}})
                    element.update(
                        score=0,
                        comments="",
                        assessor=assessor,
                        assessor_name=assessor_name,
                    )
                    return {
                        **obj,
                        change_key: element,
                    }

                item["assessor_roles"] = reduce(
                    transform_data, item["assessor_roles"], {}
                )
                item["all_assessor"] = combine_all_role
                competences.append(item)

            return Response(competences, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_evaluation_overall_comment_and_role(self, request, *args, **kwargs):
        try:
            evaluation_template_id = self.request.query_params.get(
                "evaluation_template_id", None
            )
            employee_id = self.request.query_params.get("employee_id", None)
            probation_line_manager_id = self.request.query_params.get(
                "probation_line_manager_id", None
            )
            overall_queryset = (
                EvaluationTemplateOverallCommentAssessorRole.objects.select_related(
                    "overall_comment"
                )
                .filter(overall_comment__evaluation_template_id=evaluation_template_id)
                .order_by("created_at")
            )
            overall_comments = [
                EvaluationTemplateOverallCommentAssessorRoleDepthSerializer(
                    overall,
                    context={
                        "employee_id": employee_id,
                        "probation_line_manager_id": probation_line_manager_id,
                    },
                ).data
                for overall in overall_queryset
            ]
            return Response(overall_comments, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        evaluation_template = self.get_queryset().all()
        page = self.paginate_queryset(evaluation_template)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(evaluation_template, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def list_active(self, request, *args, **kwargs):
        evaluation_template = self.get_queryset().filter(status=1)
        serializer = self.serializer_class(evaluation_template, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        evaluation_template = EvaluationTemplate.objects.get(pk=kwargs["pk"])
        serializer = EvaluationTemplateSerializer(
            evaluation_template,
            data={"status": not evaluation_template.status},
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        competencies_data = EvaluationTemplateCompetenceService.handle_data_update(
            data.get("competencies"), data.get("id")
        )
        overall_comment_data = (
            EvaluationTemplateOverallCommentService.handle_data_update(
                data.get("overall_comments"), data.get("id")
            )
        )

        with transaction.atomic():
            evaluation_template = EvaluationTemplate.objects.get(pk=data.get("id"))
            evaluation_template.name = data.get("name")
            evaluation_template.office_id = data.get("office")
            evaluation_template.type_id = data.get("type")
            evaluation_template.save()

            competencies_objs = EvaluationTemplateCompetenceService.get_list_update(
                competencies_data["competencies_update"]
            )
            EvaluationTemplateCompetence.objects.bulk_update(
                competencies_objs, ["competence"]
            )

            assessor_objs = (
                EvaluationTemplateCompetenceAssessorRoleService.get_list_update(
                    competencies_data["competencies_assessor_update"]
                )
            )
            EvaluationTemplateCompetenceAssessorRole.objects.bulk_update(
                assessor_objs, ["assessor_role"]
            )

            competencies = EvaluationTemplateCompetenceService.create_list_competence(
                competencies_data["competencies_create"], data
            )
            competence_objs = EvaluationTemplateCompetence.objects.bulk_create(
                competencies
            )

            assessor_objs_1 = EvaluationTemplateCompetenceAssessorRoleService.create_list_competence_assessor_role(
                competencies_data["competencies_create"], competence_objs
            )
            assessor_objs_2 = (
                EvaluationTemplateCompetenceAssessorRoleService.get_list_create(
                    competencies_data["competencies_assessor_create"]
                )
            )
            EvaluationTemplateCompetenceAssessorRole.objects.bulk_create(
                assessor_objs_1
            )
            EvaluationTemplateCompetenceAssessorRole.objects.bulk_create(
                assessor_objs_2
            )
            EvaluationTemplateCompetence.objects.filter(
                id__in=competencies_data["competencies_delete"]
            ).delete()
            EvaluationTemplateCompetenceAssessorRole.objects.filter(
                id__in=competencies_data["competencies_assessor_delete"]
            ).delete()

            overall_comment_objs = (
                EvaluationTemplateOverallCommentService.get_list_update(
                    overall_comment_data["overall_comment_update"]
                )
            )
            EvaluationTemplateOverallComment.objects.bulk_update(
                overall_comment_objs, ["term"]
            )

            assessor_objs = (
                EvaluationTemplateOverallCommentAssessorRoleService.get_list_update(
                    overall_comment_data["overall_comment_assessor_update"]
                )
            )
            EvaluationTemplateOverallCommentAssessorRole.objects.bulk_update(
                assessor_objs, ["overall_comment_role"]
            )

            overall_comment = (
                EvaluationTemplateOverallCommentService.create_list_overall_comment(
                    overall_comment_data["overall_comment_create"], data
                )
            )
            overall_comment_objs = EvaluationTemplateOverallComment.objects.bulk_create(
                overall_comment
            )

            assessors_objs_1 = EvaluationTemplateOverallCommentAssessorRoleService.create_list_overall_comment_assessor_role(
                overall_comment_data["overall_comment_create"], overall_comment_objs
            )
            assessors_objs_2 = (
                EvaluationTemplateOverallCommentAssessorRoleService.get_list_update(
                    overall_comment_data["overall_comment_assessor_create"]
                )
            )
            EvaluationTemplateOverallCommentAssessorRole.objects.bulk_create(
                assessors_objs_1
            )
            EvaluationTemplateOverallCommentAssessorRole.objects.bulk_create(
                assessors_objs_2
            )
            EvaluationTemplateOverallComment.objects.filter(
                id__in=overall_comment_data["overall_comment_delete"]
            ).delete()
            EvaluationTemplateOverallCommentAssessorRole.objects.filter(
                id__in=overall_comment_data["overall_comment_assessor_delete"]
            ).delete()

        return Response(
            {"success": "Evaluation Template is updated success"},
            status=status.HTTP_200_OK,
        )
