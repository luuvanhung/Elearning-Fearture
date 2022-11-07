from api_base.views import BaseViewSet
from api_skill.models import Skill
from api_skill.serializers import SkillSerializer


class SkillViewSet(BaseViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    required_alternate_scopes = {
        "retrieve": [["skill:view"]],
        "list": [["skill:view"]],
    }
