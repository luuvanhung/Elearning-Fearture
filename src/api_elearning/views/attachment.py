from api_base.views import ElearningBaseViewSet
from api_elearning.models import Attachment, Transcript
from api_elearning.serializers import AttachmentSerializer, ListLessonTranscriptSerializer
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class AttachmentViewSet(ElearningBaseViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def create(self, request, course_pk, chapter_pk, lesson_pk, *args, **kwargs):
        data = request.data.copy()
        data['last_modifier'] = request.user.id
        data['lesson_id'] = lesson_pk
        data['owner_id'] = request.user.id
        file_name = request.FILES['file'].name
        data['original_name'] = file_name
        data['path'] = "/".join(
            ['courses', str(course_pk), 'chapters', str(chapter_pk), 'lessons', str(lesson_pk), str(file_name)])
        serializer = self.serializer_class(data=data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                response['message'] = 'Attachment created!'
                return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, course_pk=None, chapter_pk=None, lesson_pk=None, *args, **kwargs):
        queryset = Attachment.objects.filter(lesson_id=lesson_pk).order_by("-created_at")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=[HttpMethod.GET], detail=True)
    def get_transcripts(self, request, pk, *args, **kwargs):
        queryset = Transcript.objects.filter(attachment_id=pk)
        res_data = ListLessonTranscriptSerializer(queryset, many=True).data
        if(res_data):
            return Response(res_data, status=status.HTTP_200_OK)
        else:
            return Response({"error_message": 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
