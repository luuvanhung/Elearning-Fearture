from datetime import datetime

from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import Assignment, Course
from api_elearning.serializers import AssignmentChapterSerializer, CourseListSerializer, QuizResultSerializer
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers
from rest_framework.fields import UUIDField


class AssignmentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=User.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='user')
    user = UserReadSerializer(required=False)
    course_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                   queryset=Course.objects.all(),
                                                   pk_field=UUIDField(format='hex'),
                                                   source='course')
    course = CourseListSerializer(required=False)
    assignment_chapters = AssignmentChapterSerializer(many=True, read_only=True, required=False)
    quiz_results = QuizResultSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'user', 'user_id', 'full_name', 'course', 'course_id', 'course_name', 'start_date',
                  'end_date', 'due_date', 'status', 'assignment_chapters', 'quiz_results']
        extra_kwargs = {
            'end_date': {'required': False},
            'start_date': {'required': True},
            'due_date': {'required': False},
            'status': {'required': False},
            'full_name': {'required': False},
            'course_name': {'required': False},
        }
        depth = 1

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['update']:
            kwargs = dict({'read_only': True})
            extra_kwargs['course_id'] = kwargs
        return extra_kwargs

    def to_internal_value(self, data):
        context = self.context
        if context.get('view') and context.get('view').action in ['create', 'get_or_create_assignment']:
            data['due_date'] = datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None
            data['start_date'] = datetime.strptime(data.get('start_date'), '%Y-%m-%d') if data.get(
                'start_date') else datetime.today()
            if data.get('due_date') and data.get('start_date') >= data.get('due_date'):
                raise Exception('The due date must be greater the start date')
        return super().to_internal_value(data)

    def to_representation(self, data):
        context = self.context
        if context.get('view') and context.get('view').action in ['retrieve']:
            user = context.get('request').user
            if not user.is_admin:
                if data.user_id != user.id:
                    raise Exception('Not your assignment.')
            data = super().to_representation(data)
            data['course_quizzes'] = data['course'].pop('course_quizzes')
            for chapter in data['assignment_chapters']:
                if chapter['status'] == AssignmentContentStatus.LOCK.value:
                    chapter['chapter'] = None
                chapter['chapter_quizzes'] = chapter['chapter'].pop('chapter_quizzes') if chapter['chapter'] else None
                for lesson in chapter['assignment_chapter_lessons']:
                    if lesson['status'] == AssignmentContentStatus.LOCK.value:
                        lesson['lesson'] = None
                        lesson['assignment_chapter_lesson_attachments'] = []
                    lesson['lesson_quizzes'] = lesson['lesson'].pop('lesson_quizzes') if lesson['lesson'] else None
        else:
            data = super().to_representation(data)
        return data


class AssignmentReadSerializer(serializers.ModelSerializer):
    assignment_chapters = AssignmentChapterSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Assignment
        fields = ['id', 'user_id', 'full_name', 'course_id', 'course_name', 'start_date',
                  'end_date', 'due_date', 'status', 'assignment_chapters']
