from api_elearning.models import QuestionType
from rest_framework import serializers


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'name']
