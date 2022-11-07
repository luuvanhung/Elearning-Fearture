from api_base.views import BaseViewSet
from api_skill.models import TitleSkill
from api_skill.serializers import TitleSkillListSerializer, TitleSkillSerializer
from api_user.models import Titles
from rest_framework import status
from rest_framework.response import Response


class TitleSkillViewSet(BaseViewSet):
    queryset = TitleSkill.objects.all()
    serializer_class = TitleSkillSerializer

    serializer_map = {"list": TitleSkillListSerializer}
    required_alternate_scopes = {
        "create": [["title_skill:edit"]],
        "retrieve": [["title_skill:view"]],
        "update": [["title_skill:edit"]],
        "destroy": [["title_skill:edit"]],
        "list": [["title_skill:view"]],
    }

    def list(self, request, *args, **kwargs):
        query_set = Titles.objects.all().order_by("title")
        serializer = self.get_serializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
