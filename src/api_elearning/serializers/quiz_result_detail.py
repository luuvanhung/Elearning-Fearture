from api_elearning.models import Question, QuestionType, QuizResult, QuizResultDetail
from api_elearning.serializers import QuestionQuizDetailSerializer, QuizResultDetailAnswerSerializer
from rest_framework import serializers
from rest_framework.fields import UUIDField


class QuizResultDetailSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                     queryset=Question.objects.all(),
                                                     pk_field=UUIDField(format='hex'),
                                                     source='question')
    question = QuestionQuizDetailSerializer(required=False)
    type_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=QuestionType.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='type')
    quiz_result_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                        queryset=QuizResult.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='quiz_result')
    quiz_result_detail_answers = QuizResultDetailAnswerSerializer(many=True, required=False)

    class Meta:
        model = QuizResultDetail
        fields = ['id', 'question', 'question_id', 'question_content', 'type_id', 'type', 'quiz_result',
                  'quiz_result_id', 'score', 'quiz_result_detail_answers']
        extra_kwargs = {
            'type': {'required': False, 'write_only': True},
            'quiz': {'required': False},
            'question_content': {'required': False},
            'quiz_result': {'required': False, 'write_only': True},
            'score': {'required': False},
        }

    def to_internal_value(self, data):
        detail_answers = data.get('quiz_result_detail_answers')
        context = self.context.get('view')
        data = super().to_internal_value(data)

        if detail_answers:
            detail_answers_serializer = QuizResultDetailAnswerSerializer(data=detail_answers, many=True,
                                                                         context=self.context)
            if detail_answers_serializer.is_valid(raise_exception=True):
                validated_data = detail_answers_serializer.validated_data
                data.update({'quiz_result_detail_answers': validated_data})
        if context and context.action in ['create']:
            question = data['question']
            data['question_content'] = question.content
            data['type'] = question.type
        return data
