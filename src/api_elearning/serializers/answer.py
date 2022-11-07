from api_elearning.models import Answer
from rest_framework import serializers


class AnswerQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'is_correct']
