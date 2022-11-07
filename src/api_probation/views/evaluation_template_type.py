from api_base.views import BaseViewSet
from api_probation.models.evaluation_template_type import EvaluationTemplateType
from api_probation.serializers.evaluation_template_type import EvaluationTemplateTypeSerializer
from rest_framework import status
from rest_framework.response import Response


class EvaluationTemplateTypeViewSet(BaseViewSet):
    queryset = EvaluationTemplateType.objects.all()
    serializer_class = EvaluationTemplateTypeSerializer
    pagination_class = None
    required_alternate_scopes = dict()

    def create(self, request, *args, **kwargs):
        serializer = EvaluationTemplateTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Your evaluation template type was updated successfully"}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Create Type Evaluation Template Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Your evaluation template type was updated successfully"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Your evaluation template type was deleted successfully"})
