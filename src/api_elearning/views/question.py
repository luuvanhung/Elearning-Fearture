from api_base.views import BaseViewSet
from api_elearning.models import Question, QuestionType
from api_elearning.serializers import QuestionQuizDetailSerializer, QuestionTypeSerializer
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class QuestionViewSet(BaseViewSet):
    serializer_class = QuestionQuizDetailSerializer
    queryset = Question.objects.all()
    serializer_map = {
        "retrieve": QuestionQuizDetailSerializer
    }

    def create(self, request, quiz_pk=None, *args, **kwargs):
        data = request.data
        if quiz_pk:
            data['quiz_id'] = quiz_pk
        question_serializer = QuestionQuizDetailSerializer(data=data)

        try:
            if question_serializer.is_valid(raise_exception=True):
                question_serializer.save()
            return Response(question_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"msg_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        q_serializer = QuestionQuizDetailSerializer(obj, data=request.data)
        try:
            if q_serializer.is_valid(raise_exception=True):
                q_serializer.save()
            return Response(QuestionQuizDetailSerializer(obj).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": str(e)})

    @action(methods=[HttpMethod.GET], detail=False)
    def retrieve_quiz_types(self, request, *args, **kwargs):
        queryset = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
