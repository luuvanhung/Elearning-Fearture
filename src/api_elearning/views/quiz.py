from api_base.views import ElearningBaseViewSet
from api_elearning.models import Quiz
from api_elearning.serializers.quiz import QuizSerializer
from rest_framework import status
from rest_framework.response import Response


class QuizViewSet(ElearningBaseViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def create(self, request, course_pk=None, chapter_pk=None, lesson_pk=None, *args, **kwargs):
        data = request.data.copy()
        data['responser_id'] = request.user.id
        if lesson_pk:
            data['lesson_id'] = lesson_pk
        elif chapter_pk:
            data['chapter_id'] = chapter_pk
        elif course_pk:
            data['course_id'] = course_pk
        quiz_serializer = QuizSerializer(data=data, context=self.get_parser_context(request))
        try:
            if quiz_serializer.is_valid(raise_exception=True):
                quiz_serializer.save()
                response = quiz_serializer.data
                response['message'] = 'Quiz created!'
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, course_pk=None, chapter_pk=None, lesson_pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        if lesson_pk:
            queryset = queryset.filter(lesson_id=lesson_pk)
        elif chapter_pk:
            queryset = queryset.filter(chapter_id=chapter_pk)
        elif course_pk:
            queryset = queryset.filter(course_id=course_pk)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
