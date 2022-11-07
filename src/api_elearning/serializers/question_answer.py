from api_elearning.models import Answer, Question
from rest_framework import serializers
from rest_framework.fields import UUIDField


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                     queryset=Question.objects.all(),
                                                     pk_field=UUIDField(format='hex'),
                                                     source='question')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_id', 'content', 'is_correct', 'order']
        extra_kwargs = {
            'question': {'required': False},
            'order': {'required': False},
        }
