from api_base.views import BaseViewSet
from api_skill.models import SkillTarget
from api_skill.serializers import SkillTargetSerializer
from api_skill.services import SkillTargetService
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError


class SkillTargetViewSet(BaseViewSet):
    queryset = SkillTarget.objects.all()
    serializer_class = SkillTargetSerializer
    required_alternate_scopes = {
        "create": [["personal_skill:edit"]],
        "retrieve": [["personal_skill:view"]],
        "update": [["personal_skill:edit"]],
        "destroy": [["personal_skill:edit"]],
        "list": [["personal_skill:view"]],
        "get_by_target_user": [["personal_skill:view"]],
    }

    def destroy(self, request, *args, **kwargs):
        skill_target_id = kwargs.get("pk")
        access_user = request.user
        if SkillTargetService.delete_record(access_user, skill_target_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "you cannot delete this record"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=[HttpMethod.GET], detail=False)
    def get_by_target_user(self, request, *args, **kwargs):
        request_params = request.query_params
        user_id = request_params.get("user_id")
        if not user_id:
            raise ValidationError({"details": "Cannot find user id in url"})
        query_set = self.get_queryset().filter(target_user=user_id)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)
