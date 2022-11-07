from api_base.views import BaseViewSet
from api_skill.models import SkillLevel
from api_skill.serializers import SkillLevelSerializer


class SkillLevelViewSet(BaseViewSet):
    queryset = SkillLevel.objects.all()
    serializer_class = SkillLevelSerializer
    required_alternate_scopes = {
        "create": [["skill_level:edit"]],
        "retrieve": [["skill_level:view"]],
        "update": [["skill_level:edit"]],
        "destroy": [["skill_level:edit"]],
        "list": [["skill_level:view"]],
    }
