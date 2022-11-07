from rest_framework import serializers
from rest_framework.fields import UUIDField

from api_elearning.models import Assignment, AssignmentChapter, Chapter
from api_elearning.serializers import (
    AssignmentChapterLessonSerializer,
    ChapterAttachmentSerializer,
    QuizResultSerializer,
)


class AssignmentChapterSerializer(serializers.ModelSerializer):
    assignment_id = serializers.PrimaryKeyRelatedField(required=False,
                                                       queryset=Assignment.objects.all(),
                                                       pk_field=UUIDField(format='hex'),
                                                       source='assignment')
    chapter_id = serializers.PrimaryKeyRelatedField(required=False,
                                                    queryset=Chapter.objects.all(),
                                                    pk_field=UUIDField(format='hex'),
                                                    source='chapter')
    chapter = ChapterAttachmentSerializer(required=False)
    assignment_chapter_lessons = AssignmentChapterLessonSerializer(many=True, read_only=True)
    quiz_results = QuizResultSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = AssignmentChapter
        fields = ['id', 'assignment_id', 'chapter_id', 'chapter', 'chapter_name', 'start_date',
                  'end_date', 'status', 'assignment_chapter_lessons', 'previous_assignment_chapter_id', 'quiz_results']
        extra_kwargs = {
            # 'assignment': {'required': False, 'read_only': True},
            'chapter_name': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
        }

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['update']:
            kwargs = dict({'read_only': True})
            extra_kwargs['chapter_id'] = kwargs
            extra_kwargs['assignment_id'] = kwargs

        return extra_kwargs
