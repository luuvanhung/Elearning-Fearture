import uuid

from api_base.services import SendMail, SlackResponseService
from api_base.views import BaseViewSet
from api_probation.models import Probation, ProbationCompetence, ProbationOverallComment
from api_probation.serializers.probation import (
    CreateProbationSerializer,
    ListProbationSerializer,
    ProbationSerializer,
)
from api_probation.serializers.probation_competence import (
    ProbationCompetenceSerializer,
    UpdateProbationCompetenceSerializer,
)
from api_probation.serializers.probation_overall_comment import (
    ProbationOverallCommentSerializer,
    UpdateProbationOverallCommentSerializer,
)
from api_slackbot.services.slack.response import SubComponentBuilder
from api_team.models import TeamMembers
from api_user.services import ProfileService, UserService
from common.constants.probation_constant import AssessorRoleConstant
from django.conf import settings
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response


class ProbationViewSet(BaseViewSet):
    queryset = Probation.objects
    serializer_class = ProbationSerializer
    required_alternate_scopes = {
        "create": [["probation:create"]],
        "retrieve": [["probation:view"]],
        "update": [["probation:edit"]],
        "destroy": [["probation:destroy"]],
        "list": [["probation:view"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = None
        office = self.request.query_params.get("office")
        name = self.request.query_params.get("name")
        evaluation_type = self.request.query_params.get("type")
        filter_args = dict()
        if office:
            filter_args.update(employee__profile__office=office)
        if name:
            filter_args.update(
                employee__profile__name__icontains=Collate(
                    Value(name.strip()), "utf8mb4_general_ci"
                )
            )
        if evaluation_type:
            filter_args.update(evaluation_template__type=evaluation_type)
        competence_probation_ids = ProbationCompetence.objects.filter(
            assessor_id=request.user.id
        ).values("probation_id")
        overall_probation_ids = ProbationOverallComment.objects.filter(
            assessor_id=request.user.id
        ).values("probation_id")
        if request.user.admin:
            queryset = self.get_queryset().filter(**filter_args).order_by("-created_at")
        else:
            queryset = (
                self.get_queryset()
                .filter(
                    Q(**filter_args),
                    Q(id__in=competence_probation_ids)
                    | Q(id__in=overall_probation_ids)
                    | Q(probation_line_manager=request.user.id),
                )
                .order_by("-created_at")
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListProbationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        probation = get_object_or_404(Probation, pk=kwargs.get("pk"))
        serializer = self.serializer_class(probation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        competencies = data.get("competencies", [])
        overall_comments = data.get("overall_comments", [])
        employee_id = data.get("employee", None)
        employee = UserService.get_user_by_id(employee_id)
        employee_profile = ProfileService.get_profile_by_user_id(employee_id)

        if employee_id is None:
            return Response(
                {"error": "Please input employee name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        team_member = TeamMembers.objects.filter(member_id=employee_id).first()
        if team_member:
            data.update(team=team_member.team_id)
        try:
            with transaction.atomic():
                probation_serializer = CreateProbationSerializer(data=data)
                if probation_serializer.is_valid(raise_exception=True):
                    probation_serializer.save()
                probation_id = probation_serializer.data.get("id")
                competence_serializer = ProbationCompetenceSerializer(
                    data=competencies,
                    many=True,
                    context={"probation_id": probation_id, "employee_id": employee_id},
                )
                comment_serializer = ProbationOverallCommentSerializer(
                    data=overall_comments,
                    many=True,
                    context={"probation_id": probation_id, "employee_id": employee_id},
                )

                if competence_serializer.is_valid(raise_exception=True):
                    self.perform_create(competence_serializer)
                if comment_serializer.is_valid(raise_exception=True):
                    self.perform_create(comment_serializer)

                base_link = request.build_absolute_uri("/evaluations")
                probation_link = f"{base_link}/{probation_id}"
                employee_email_content = render_to_string(
                    "../templates/new_probation_employee.html",
                    {"link": probation_link, "user_name": employee_profile.name},
                )
                employee_slack_notify_message = (
                    f":wave: Dear *{employee_profile.name}*,\n>"
                    f" *Your evaluation is now available*\n>"
                    f"*<{probation_link}|Please visit this page to make your self-evaluation first!>*"
                )
                SendMail.start(
                    [employee.email], "New evaluation!", employee_email_content
                )

                if employee_profile.slack_id:
                    SlackResponseService(
                        channel=employee_profile.slack_id
                    ).send_message(
                        text="New evaluation available!",
                        blocks=[
                            SubComponentBuilder().section_mrkdwn_text_builder(
                                mrkdwn_text=employee_slack_notify_message
                            )
                        ],
                    )

                return Response({"msg": "success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(str(e))
            return Response(
                {"error": "New evaluation created error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        competencies = request_data.get("competencies", [])
        overall_comments = request_data.get("overall_comments", [])
        probation_line_manager = request_data.get("probation_line_manager", None)
        employee_id = request_data.get("employee_id", None)
        probation_serializer = self.get_serializer(
            request_data, request_data, partial=True
        )
        if probation_serializer.is_valid(raise_exception=True):
            self.perform_update(probation_serializer)

        try:
            with transaction.atomic():
                competence_serializer = UpdateProbationCompetenceSerializer(
                    competencies,
                    data=competencies,
                    many=True,
                    partial=True,
                    context={"probation_line_manager": probation_line_manager},
                )
                if competence_serializer.is_valid(raise_exception=True):
                    self.perform_update(competence_serializer)

                overall_serializer = UpdateProbationOverallCommentSerializer(
                    overall_comments,
                    data=overall_comments,
                    many=True,
                    partial=True,
                    context={"probation_line_manager": probation_line_manager},
                )
                if overall_serializer.is_valid(raise_exception=True):
                    self.perform_update(overall_serializer)

                evaluate_data = competencies + overall_comments
                if request.user.id == uuid.UUID(employee_id):
                    if self.check_completed_self_evaluation(
                        evaluate_data=evaluate_data,
                        employee_id=employee_id,
                    ):
                        assessors_info = []
                        for evaluate_item in evaluate_data:
                            assessor = evaluate_item.get("assessor")
                            competence_role = evaluate_item.get("competence_role")
                            overall_role = (
                                evaluate_item.get(
                                    "evaluation_template_overall_comment_assessor_role"
                                ).get("overall_comment_role")
                                if evaluate_item.get(
                                    "evaluation_template_overall_comment_assessor_role"
                                )
                                else None
                            )

                            if assessor:
                                if (
                                    competence_role != AssessorRoleConstant.SELF_ROLE
                                    and overall_role != AssessorRoleConstant.SELF_ROLE
                                ):
                                    assessors_info.append(assessor)

                        base_link = request.build_absolute_uri("/evaluations")
                        probation_link = f"{base_link}/{request_data.get('id')}"

                        assessor_email_content = render_to_string(
                            "../templates/new_probation_assessor.html",
                            {
                                "link": probation_link,
                                "user_name": request_data.get("employee")
                                .get("profile")
                                .get("name"),
                            },
                        )
                        assessor_emails = UserService.get_list_emails_by_ids(
                            [
                                assessor_info.get("id")
                                for assessor_info in assessors_info
                            ]
                        )
                        SendMail.start(
                            assessor_emails,
                            f"New Evaluation That You May Need To Take A Look!",
                            assessor_email_content,
                        )

                        slack_response_service = SlackResponseService(
                            settings.SLACK_DEFAULT_CHANNEL
                        )

                        for assessor_info in assessors_info:
                            if assessor_info.get("profile").get("slack_id") is not None:
                                assessor_slack_notify_message = (
                                    f":wave: Dear *{assessor_info.get('profile').get('name')}*,\n>"
                                    f" *{request_data.get('employee').get('profile').get('name')}* has finished the self-evaluation\n>"
                                    f"*<{probation_link}|Please visit this page to your evaluation for him(her)!>*"
                                )
                                slack_response_service.send_message(
                                    text="Evaluation available!",
                                    blocks=[
                                        SubComponentBuilder().section_mrkdwn_text_builder(
                                            mrkdwn_text=assessor_slack_notify_message
                                        )
                                    ],
                                    channel=assessor_info.get("profile").get(
                                        "slack_id"
                                    ),
                                )
                            else:
                                assessor_slack_notify_message = (
                                    f":wave: Dear all,\n>"
                                    f" *{request_data.get('employee').get('profile').get('name')}* has finished the self-evaluation\n>"
                                    f"*<{probation_link}|Please visit this page to your evaluation for him(her)!>*"
                                )
                                slack_response_service.send_message(
                                    text="Evaluation available!",
                                    blocks=[
                                        SubComponentBuilder().section_mrkdwn_text_builder(
                                            mrkdwn_text=assessor_slack_notify_message
                                        )
                                    ],
                                )

                return Response({"msg": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your evaluation updated error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def check_completed_self_evaluation(evaluate_data, employee_id):
        for evaluation_item in evaluate_data:
            if evaluation_item.get("assessor_id") == employee_id:
                if (
                    evaluation_item.get("comments") == ""
                    or evaluation_item.get("score") == 0
                ):
                    return False
        return True
