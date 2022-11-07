from api_base.views import BaseViewSet
from api_elearning.models import AssignmentChapter
from api_elearning.serializers import AssignmentChapterSerializer


class AssignmentChapterViewSet(BaseViewSet):
    queryset = AssignmentChapter.objects.all()
    serializer_class = AssignmentChapterSerializer
