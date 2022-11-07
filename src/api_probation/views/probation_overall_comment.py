from api_base.views import BaseViewSet
from api_probation.models import ProbationOverallComment
from api_probation.serializers import ProbationOverallCommentSerializer
from api_probation.serializers.probation_overall_comment import (
    ListProbationOverallCommentSerializer,
)
from rest_framework import status
from rest_framework.response import Response


class ProbationOverallCommentViewSet(BaseViewSet):
    queryset = ProbationOverallComment.objects
    serializer_class = ProbationOverallCommentSerializer
    required_alternate_scopes = {}

    def list(self, request, *args, **kwargs):
        probation_overall_comments = self.queryset.all()
        serializer = ListProbationOverallCommentSerializer(
            probation_overall_comments, many=True
        )
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
