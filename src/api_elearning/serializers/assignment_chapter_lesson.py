from api_elearning.models import AssignmentChapter, Lesson
from api_elearning.models.assignment import AssignmentChapterLesson
from api_elearning.serializers import (
    AssignmentChapterLessonAttachmentSerializer,
    LessonReadSerializer,
    QuizResultSerializer,
)
from rest_framework import serializers
from rest_framework.fields import UUIDField


class AssignmentChapterLessonSerializer(serializers.ModelSerializer):
    assignment_chapter_id = serializers.PrimaryKeyRelatedField(required=False,
                                                               queryset=AssignmentChapter.objects.all(),
                                                               pk_field=UUIDField(format='hex'),
                                                               source='assignment_chapter')
    lesson_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                                   queryset=Lesson.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='lesson')
    lesson = LessonReadSerializer(required=False, read_only=True)
    assignment_chapter_lesson_attachments = AssignmentChapterLessonAttachmentSerializer(read_only=True, many=True)
    quiz_results = QuizResultSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = AssignmentChapterLesson
        fields = ['id', 'assignment_chapter_id', 'lesson_id', 'lesson', 'lesson_name', 'lesson',
                  'assignment_chapter_lesson_attachments', 'previous_assignment_chapter_lesson_id',
                  'completed_lesson_content', 'quiz_results',
                  'start_date', 'end_date', 'status', 'assignment_chapter_lesson_attachments']
        extra_kwargs = {
            'lesson_name': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'completed_lesson_content': {'required': False},
        }

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['update']:
            kwargs = dict({'read_only': True})
            extra_kwargs['assignment_chapter_id'] = kwargs
            extra_kwargs['lesson_id'] = kwargs
        return extra_kwargs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return super().to_representation(instance)
