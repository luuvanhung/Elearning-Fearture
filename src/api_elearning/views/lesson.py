from api_base.views import BaseViewSet
from api_elearning.models import Lesson
from api_elearning.serializers import LessonReadSerializer, LessonSerializer
from rest_framework import status
from rest_framework.response import Response


class LessonViewSet(BaseViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    serializer_map = {"retrieve": LessonReadSerializer}

    def create(self, request, course_pk, chapter_pk, *args, **kwargs):
        data = request.data.copy()
        data['last_modifier_id'] = request.user.id
        data['chapter_id'] = chapter_pk

        serializer = self.serializer_class(data=data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, course_pk, chapter_pk, *args, **kwargs):
        data = request.data.copy()
        data['chapter_id'] = chapter_pk
        data['last_modifier_id'] = request.user.id
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(LessonReadSerializer(obj).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
