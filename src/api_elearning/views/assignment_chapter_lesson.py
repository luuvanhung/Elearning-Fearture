from api_base.views import BaseViewSet
from api_elearning.models.assignment import AssignmentChapterLesson
from api_elearning.serializers import AssignmentChapterLessonSerializer


class AssignmentChapterLessonViewSet(BaseViewSet):
    queryset = AssignmentChapterLesson.objects.all()
    serializer_class = AssignmentChapterLessonSerializer
