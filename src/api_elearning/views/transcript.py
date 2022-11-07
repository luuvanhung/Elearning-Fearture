from rest_framework import status
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_elearning.models import Transcript
from api_elearning.serializers import TranscriptSerializer
from api_elearning.services import TranscriptService


class TranscriptViewSet(BaseViewSet):
    serializer_class = TranscriptSerializer
    queryset = Transcript.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        attachment_id = data.get("attachment_id", "")
        transcripts = data.get("transcripts", [])
        try:
            response = TranscriptService.bulk_create(attachment_id, transcripts)
        except Exception as e:
            return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)
