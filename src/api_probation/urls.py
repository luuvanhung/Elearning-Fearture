from api_probation.views.evaluation_template import EvaluationTemplateViewSet
from api_probation.views.evaluation_template_competence import (
    EvaluationTemplateCompetenceViewSet,
)
from api_probation.views.evaluation_template_competence_assessor_role import (
    EvaluationTemplateCompetenceAssessorRoleViewSet,
)
from api_probation.views.evaluation_template_type import EvaluationTemplateTypeViewSet
from api_probation.views.probation import ProbationViewSet
from api_probation.views.probation_competence import ProbationCompetenceViewSet
from api_probation.views.probation_overall_comment import ProbationOverallCommentViewSet
from api_probation.views.probation_reminder import ProbationReminderViewSet
from rest_framework.routers import SimpleRouter

app_name = "api_probation"

router = SimpleRouter(trailing_slash=False)
router.register(
    r"overall-comment",
    ProbationOverallCommentViewSet,
    basename="probation_overall_comment",
)
router.register(
    r"competence", ProbationCompetenceViewSet, basename="probation_competence"
)
router.register(
    r"evaluation_template/competence",
    EvaluationTemplateCompetenceViewSet,
    basename="evaluation_template_competence",
)
router.register(
    r"evaluation_template/competence_assessor_role",
    EvaluationTemplateCompetenceAssessorRoleViewSet,
    basename="evaluation_template_competence",
)
router.register(
    r"evaluation_template_type",
    EvaluationTemplateTypeViewSet,
    basename="evaluation_template_type",
)
router.register(
    r"evaluation_template", EvaluationTemplateViewSet, basename="evaluation_template"
)
router.register(r"reminder", ProbationReminderViewSet, basename="probation_reminder")
router.register(r"", ProbationViewSet, basename="probation_detail")
urlpatterns = router.urls
