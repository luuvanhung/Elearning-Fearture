from api_elearning.models import Question, QuestionType, Quiz
from api_elearning.serializers import AnswerQuizSerializer, QuestionTypeSerializer
from api_elearning.serializers.question_answer import QuestionAnswerSerializer
from api_elearning.services import QuestionService
from rest_framework import serializers
from rest_framework.fields import UUIDField


class QuestionQuizDetailSerializer(serializers.ModelSerializer):
    question_answers = AnswerQuizSerializer(many=True, read_only=True)
    quiz_id = serializers.PrimaryKeyRelatedField(required=False,
                                                 queryset=Quiz.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='quiz')
    type_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=QuestionType.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='type')
    type = QuestionTypeSerializer(required=False, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz_id', 'content', 'score', 'type_id', 'type', 'order', 'question_answers']
        extra_kwargs = {
            'order': {'required': False},
        }

    def to_internal_value(self, data):
        data = data.copy()
        data.update({'type_id': data.pop('type').get('id')})
        question_quiz_serializer = QuestionAnswerSerializer(data=data.get('question_answers'), many=True)
        if question_quiz_serializer.is_valid(raise_exception=True):
            question_validate = question_quiz_serializer.validated_data
            data = super().to_internal_value(data)
            data.update({'question_answers': question_validate})
        else:
            raise Exception('Your answer is invalid')
        return data

    def create(self, validated_data):
        return QuestionService.create_questions(validated_data)

    def update(self, instance, validated_data):
        return QuestionService.update_questions(instance, validated_data)

    def get_extra_kwargs(self):
        context = self.context.get('view')
        extra_kwargs = super().get_extra_kwargs()
        if context and context.action in ['update']:
            kwargs = dict({'read_only': True})
            kwargs_required = dict({'required': True})
            extra_kwargs['quiz_id'] = kwargs
            extra_kwargs['order'] = kwargs
            extra_kwargs['id'] = kwargs_required
        return extra_kwargs


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'content', 'score', 'type', 'quiz']
