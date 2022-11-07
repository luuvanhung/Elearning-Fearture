from api_base.views import BaseViewSet
from api_skill.models import SkillVote
from api_skill.serializers import CreateSkillVoteSerializer, ListSkillVoteSerializer
from api_skill.services import SkillVoteService
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class SkillVoteViewSet(BaseViewSet):
    queryset = SkillVote.objects.all()
    serializer_map = {
        "create": CreateSkillVoteSerializer,
        "update": CreateSkillVoteSerializer,
        "patch": CreateSkillVoteSerializer,
        "list": ListSkillVoteSerializer,
        "search": ListSkillVoteSerializer,
        "get_current_skills": ListSkillVoteSerializer,
        "vote_skills": CreateSkillVoteSerializer,
        "report": ListSkillVoteSerializer,
    }
    required_alternate_scopes = {
        "create": [["personal_skill:edit"]],
        "retrieve": [["personal_skill:view"]],
        "update": [["personal_skill:edit"]],
        "destroy": [["personal_skill:edit"]],
        "vote_skills": [["personal_skill:edit"]],
        "list": [["personal_skill:view"]],
        "search": [["personal_skill:view"]],
        "get_current_skills": [["personal_skill:view"]],
        "report": [["personal_skill:view"]],
    }
    """
    @api skill_report
    @apiAction /api/v1/skill/report
    @apiPermission {any}
    @apiParam {none}
    @apiSuccessExample
        {

        }
    """

    def destroy(self, request, *args, **kwargs):
        skill_vote_id = kwargs.get("pk")
        access_user = request.user
        if SkillVoteService.delete_record(access_user, skill_vote_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "you cannot delete this record"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=[HttpMethod.GET], detail=False)
    def search(self, request, *args, **kwargs):
        request_params = request.query_params
        total_records, query_set = SkillVoteService.get_all(request_params)
        serializer = self.get_serializer(query_set, many=True)
        result = serializer.data
        return Response({"data": result, "total_records": total_records})

    @action(methods=[HttpMethod.GET], detail=False)
    def get_current_skills(self, request, *args, **kwargs):
        request_params = request.query_params
        user_id = request_params.get("user_id")
        if not user_id:
            raise ValidationError({"details": "Cannot find user id in url"})
        query_set = SkillVoteService.get_current_skills(user_id)
        return Response(query_set)

    @action(methods=[HttpMethod.POST], detail=False)
    def vote_skills(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=[HttpMethod.GET], detail=False)
    def report(self, request, *args, **kwargs):
        self.queryset = SkillVoteService.count_level_skill()
        rs = self.get_serializer(self.get_queryset(), many=True)

        return Response(data=rs.data, status=status.HTTP_200_OK)
