from api_user.models import Titles
from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=50)

    class Meta:
        model = Titles
        fields = ["id", "title"]
