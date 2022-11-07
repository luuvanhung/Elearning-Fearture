from api_elearning.models import Chapter, Course, Lesson, Quiz
from api_elearning.serializers import QuestionQuizDetailSerializer
from api_elearning.services import QuizService
from api_user.models import User
from api_user.serializers import UserVoteSerializer
from rest_framework import serializers


class QuizSerializer(serializers.ModelSerializer):
    lesson_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Lesson.objects.all(), source='lesson')
    chapter_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Chapter.objects.all(), source='chapter')
    course_id = serializers.PrimaryKeyRelatedField(required=False, queryset=Course.objects.all(), source='course')
    responser_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                      source='responser')
    responser = UserVoteSerializer(required=False)
    quiz_questions = QuestionQuizDetailSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'lesson_id', 'chapter_id', 'course_id', 'description', 'shuffled', 'threshold',
                  'responser', 'responser_id', 'quiz_questions']

    def to_internal_value(self, data):
        context = self.context.get('view')
        quiz_questions = data.get('quiz_questions')
        if context and context.action in ['create']:
            if data.get('quiz_questions'):
                question_quiz_serializer = QuestionQuizDetailSerializer(data=data.get('quiz_questions'), many=True,
                                                                        context=self.context)
                if question_quiz_serializer.is_valid(raise_exception=True):
                    quiz_questions = question_quiz_serializer.validated_data

        if (data.get('course_id') is None and data.get('chapter_id') is None) or (
                data.get('lesson_id') is None and data.get('chapter_id') is None) or (
                data.get('course_id') is None and data.get('lesson_id') is None):
            data = super().to_internal_value(data)
            data.update({'quiz_questions': quiz_questions})
        else:
            raise Exception('Only one foreign key field can set value')
        return data

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        context = self.context
        if context.get('view') and context.get('view').action in ['retrieve'] \
                and instance.get('responser') \
                and instance.get('responser')['id'].hex != self.context.get('request').user.id.hex:
            questions = instance.get('quiz_questions')
            [[answer.pop('is_correct') for answer in question.get('question_answers')] for question in questions if
             questions]
        return instance

    def create(self, validated_data):
        return QuizService.create_multiple_questions(validated_data)

    def update(self, instance, validated_data):
        return QuizService.update_question(instance, validated_data)

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['update']:
            kwargs = dict({'read_only': True})
            extra_kwargs['course_id'] = kwargs
            extra_kwargs['chapter_id'] = kwargs
            extra_kwargs['lesson_id'] = kwargs
        return extra_kwargs


class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'threshold', 'quiz_questions']
