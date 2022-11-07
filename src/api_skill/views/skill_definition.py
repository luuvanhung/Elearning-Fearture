from api_base.views import BaseViewSet
from api_skill.models import Skill, SkillDefinition
from api_skill.serializers import SkillDefinitionSerializer
from api_skill.services import SkillDefinitionService
from common import Utils
from common.constants.api_constants import HttpMethod
from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class SkillDefinitionViewSet(BaseViewSet):
    queryset = SkillDefinition.objects.all()
    serializer_class = SkillDefinitionSerializer
    required_alternate_scopes = {
        "create": [["skill_definition:edit"]],
        "retrieve": [["skill_definition:view"]],
        "update": [["skill_definition:edit"]],
        "destroy": [["skill_definition:edit"]],
        "list": [["skill_definition:view"]],
        "delete_by_skill_id": [["skill_definition:edit"]],
        "create_multiple_skill_definition": [["skill_definition:edit"]],
        "get_levels_by_skill_id": [["skill_definition:view"]],
        "get_all": [["skill_definition:view"]],
    }

    @action(methods=[HttpMethod.DELETE], detail=False)
    def delete_by_skill_id(self, request, *args, **kwargs):
        skill_id = Utils.cast_to_int(request.query_params.get("skill_id"))
        is_deleted = SkillDefinitionService.delete_by_skill_id(skill_id)
        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Cannot delete all of these records"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=[HttpMethod.POST], detail=False)
    def create_multiple_skill_definition(self, request, *args, **kwargs):
        data = request.data

        skill_name = data.get("skill_name", "")
        skill_definitions = data.get("skill_definitions", [])
        if not skill_name:
            return Response(
                {"detail": "skill name field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not skill_definitions:
            return Response(
                {"detail": "skill_definitions field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Skill.objects.filter(name=skill_name).exists():
            return Response(
                {"detail": "This skill name already existed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        level_ids = []
        for skill_definition in skill_definitions:
            level_id = skill_definition.get("level", {}).get("id", 0)
            if not level_id:
                return Response(
                    {"detail": "level id is empty"}, status=status.HTTP_400_BAD_REQUEST
                )
            level_ids.append(level_id)
        if len(level_ids) > len(set(level_ids)):
            return Response(
                {"detail": "level ids is duplicated"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            skill = Skill.objects.create(name=skill_name)
            for skill_definition in skill_definitions:
                skill_definition["skill"] = skill.__dict__

            serializer = SkillDefinitionSerializer(data=skill_definitions, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_levels_by_skill_id(self, request, *args, **kwargs):
        skill_id = request.query_params.get("skill_id")
        levels = SkillDefinition.objects.filter(skill_id=skill_id).values(
            "id",
            "level_id",
            level_name=F("level__name"),
            level_weight=F("level__weight"),
        )
        if not levels.exists():
            return Response(
                {"detail": "This skill id doesn't have any corresponding level id"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(levels, status=status.HTTP_200_OK)
