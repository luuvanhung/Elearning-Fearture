from api_elearning.models import Answer, QuizResultDetailAnswer
from api_elearning.serializers import AnswerQuizSerializer
from rest_framework import serializers
from rest_framework.fields import UUIDField


class QuizResultDetailAnswerSerializer(serializers.ModelSerializer):
    answer_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                   queryset=Answer.objects.all(),
                                                   pk_field=UUIDField(format='hex'),
                                                   source='answer')
    quiz_result_detail_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                               queryset=QuizResultDetailAnswer.objects.all(),
                                                               pk_field=UUIDField(format='hex'),
                                                               source='quiz_result_detail')
    answer = AnswerQuizSerializer(required=False)

    class Meta:
        model = QuizResultDetailAnswer
        fields = ['id', 'answer_id', 'answer', 'answer_content', 'correct', 'chosen', 'quiz_result_detail',
                  'quiz_result_detail_id']
        extra_kwargs = {
            'answer_content': {'required': False, 'write_only': True},
            'chosen': {'required': False},
            'quiz_result_detail': {'required': False, 'write_only': True},
        }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        context = self.context.get('view')
        if context and context.action in ['create']:
            answer = data['answer']
            data['answer_content'] = answer.content
        return data
