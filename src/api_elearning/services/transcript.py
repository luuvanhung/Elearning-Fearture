import string
from typing import List

from api_base.services import BaseService
from api_elearning.models import Transcript
from api_elearning.serializers import TranscriptSerializer


class TranscriptService(BaseService):
    @classmethod
    def bulk_create(cls, lesson_id: string, transcripts: dict) -> List[Transcript]:
        serializer = TranscriptSerializer(data=transcripts, many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
        new_transcripts = [
            Transcript(time=transcript.get("script_at_second", ""), content=transcript.get("content", ""), lesson_id=lesson_id) for
            transcript in validated_data]
        result = Transcript.objects.bulk_create(new_transcripts)
        res_data = TranscriptSerializer(result, many=True).data
        return res_data
