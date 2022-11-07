from api_elearning.models import Topic
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class TopicTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']
