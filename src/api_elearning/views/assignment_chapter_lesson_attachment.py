from api_base.views import BaseViewSet
from api_elearning.models import AssignmentChapterLessonAttachment
from api_elearning.serializers import AssignmentChapterLessonAttachmentSerializer


class AssignmentChapterLessonAttachmentViewSet(BaseViewSet):
    queryset = AssignmentChapterLessonAttachment.objects.all()
    serializer_class = AssignmentChapterLessonAttachmentSerializer
