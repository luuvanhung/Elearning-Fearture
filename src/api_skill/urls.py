from rest_framework import routers

from .views import (
    SkillDefinitionViewSet,
    SkillLevelViewSet,
    SkillTargetViewSet,
    SkillViewSet,
    SkillVoteViewSet,
    TitleSkillViewSet,
)

app_name = "api_skill"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"level", SkillLevelViewSet, basename="skill_level")
router.register(r"definition", SkillDefinitionViewSet, basename="skill_definition")
router.register(r"title", TitleSkillViewSet, basename="title_skill")
router.register(r"vote", SkillVoteViewSet, basename="skill_vote")
router.register(r"target", SkillTargetViewSet, basename="skill_target")
router.register(r"", SkillViewSet, basename="skill")

urlpatterns = router.urls
