from api_base.views import BaseViewSet
from api_probation.models import ProbationCompetence
from api_probation.serializers import ProbationCompetenceSerializer
from api_probation.serializers.probation_competence import (
    ListProbationCompetenceSerializer,
)
from rest_framework import status
from rest_framework.response import Response


class ProbationCompetenceViewSet(BaseViewSet):
    queryset = ProbationCompetence.objects
    serializer_class = ProbationCompetenceSerializer
    required_alternate_scopes = {}

    def list(self, request, *args, **kwargs):
        probation_competences = self.queryset.all()
        serializer = ListProbationCompetenceSerializer(probation_competences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            try:
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error_msg": str(e)})
