from api_elearning.models import Assignment, AssignmentChapter, AssignmentChapterLesson, Quiz, QuizResult
from api_elearning.serializers import QuizSerializer
from api_elearning.serializers.quiz_result_detail import QuizResultDetailSerializer
from api_elearning.services import QuizResultService
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers


class QuizResultSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                 source='user')
    user = UserReadSerializer(required=False)
    quiz_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Quiz.objects.all(),
                                                 source='quiz')
    assignment_chapter_lesson_id = serializers.PrimaryKeyRelatedField(required=False,
                                                                      queryset=AssignmentChapterLesson.objects.all(),
                                                                      source='assignment_chapter_lesson')
    assignment_chapter_id = serializers.PrimaryKeyRelatedField(required=False, queryset=AssignmentChapter.objects.all(),
                                                               source='assignment_chapter')
    assignment_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Assignment.objects.all(),
                                                       source='assignment')
    quiz = QuizSerializer(read_only=True, required=False)
    quiz_result_details = QuizResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = QuizResult
        fields = ['id', 'user_id', 'user', 'quiz_id', 'quiz', 'quiz_title', 'assignment_id', 'assignment',
                  'assignment_chapter_id', 'assignment_chapter', 'assignment_chapter_lesson_id', 'full_name',
                  'assignment_chapter_lesson', 'threshold', 'is_passed','quiz_result_details']
        extra_kwargs = {
            'user': {'required': False},
            'quiz': {'required': False},
            'quiz_title': {'required': False},
            'assignment_chapter_lesson': {'required': False, 'write_only': True},
            'assignment_chapter': {'required': False, 'write_only': True},
            'assignment': {'required': False, 'write_only': True},
            'full_name': {'required': False},
            'threshold': {'required': False},
            'is_passed': {'required': False},
        }

    def create(self, validated_data):
        return QuizResultService.create_quiz_result(validated_data)

    def to_internal_value(self, data):
        context = self.context.get('view')
        quiz_result_details = data.get('quiz_result_details')
        data = super().to_internal_value(data)

        if quiz_result_details:
            question_quiz_serializer = QuizResultDetailSerializer(data=quiz_result_details, many=True,
                                                                  context=self.context)
            if question_quiz_serializer.is_valid(raise_exception=True):
                validated_data = question_quiz_serializer.validated_data
                data.update({'quiz_result_details': validated_data})

        if context and context.action in ['create']:
            quiz = data['quiz']
            data['quiz_title'] = quiz.title
            data['assignment_chapter_lesson'] = data.get('assignment_chapter_lesson') if data.get(
                'assignment_chapter_lesson') else None
            data['assignment_chapter'] = data.get('assignment_chapter') if data.get('assignment_chapter') else None
            data['assignment'] = data.get('assignment') if data.get('assignment') else None
            data['threshold'] = quiz.threshold
            data['full_name'] = data.get('user').profile.name

        return data
