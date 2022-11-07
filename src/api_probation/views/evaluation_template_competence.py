from api_base.views import BaseViewSet
from api_probation.models import EvaluationTemplateCompetence
from api_probation.serializers import EvaluationTemplateCompetenceSerializer


class EvaluationTemplateCompetenceViewSet(BaseViewSet):
    queryset = EvaluationTemplateCompetence.objects.all()
    pagination_class = None
    serializer_class = EvaluationTemplateCompetenceSerializer
    required_alternate_scopes = {}
