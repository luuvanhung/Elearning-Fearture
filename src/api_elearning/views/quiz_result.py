from api_base.views import BaseViewSet
from api_elearning.models.quiz_result import QuizResult
from api_elearning.serializers import QuizResultSerializer, QuizSerializer
from api_elearning.services import QuizResultService
from rest_framework import status
from rest_framework.response import Response


class QuizResultViewSet(BaseViewSet):
    serializer_class = QuizResultSerializer
    queryset = QuizResult.objects.all()

    def create(self, request, assignment_pk=None, chapter_pk=None, lesson_pk=None, quiz_pk=None, *args,
               **kwargs):
        data = request.data.copy()
        data['user_id'] = request.user.id
        if quiz_pk:
            data['quiz_id'] = quiz_pk
        if lesson_pk:
            data['assignment_chapter_lesson_id'] = lesson_pk
        elif chapter_pk:
            data['assignment_chapter_id'] = chapter_pk
        elif assignment_pk:
            data['assignment_id'] = assignment_pk
        quiz_serializer = QuizResultSerializer(data=data, context=self.get_parser_context(request))

        try:
            if quiz_serializer.is_valid(raise_exception=True):
                validated_data = quiz_serializer.validated_data
                quiz = QuizSerializer(validated_data['quiz']).data
                res_data = QuizResultService.create_quiz_result(validated_data, quiz)
                return Response(self.serializer_class(res_data).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
