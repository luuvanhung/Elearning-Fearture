from api_base.views import BaseViewSet
from api_probation.models import EvaluationTemplateCompetenceAssessorRole
from api_probation.serializers import EvaluationTemplateCompetenceAssessorRoleSerializer


class EvaluationTemplateCompetenceAssessorRoleViewSet(BaseViewSet):
    queryset = EvaluationTemplateCompetenceAssessorRole.objects.all()
    pagination_class = None
    serializer_class = EvaluationTemplateCompetenceAssessorRoleSerializer
    required_alternate_scopes = {}
