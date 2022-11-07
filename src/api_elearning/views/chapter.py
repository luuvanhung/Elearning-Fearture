from api_base.views import ElearningBaseViewSet
from api_elearning.models import Chapter
from api_elearning.serializers import ChapterReadSerializer, ChapterSerializer
from rest_framework import status
from rest_framework.response import Response


class ChapterViewSet(ElearningBaseViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    serializer_map = {
        "retrieve": ChapterReadSerializer
    }

    def create(self, request, course_pk, *args, **kwargs):
        data = request.data.copy()
        data['last_modifier_id'] = request.user.id
        data['course_id'] = course_pk
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                response['message'] = 'Chapter created!'
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, course_pk, *args, **kwargs):
        data = request.data.copy()
        data['last_modifier_id'] = request.user.id
        data['course_id'] = course_pk
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = ChapterReadSerializer(instance).data
                response['message'] = 'Chapter updated!'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
