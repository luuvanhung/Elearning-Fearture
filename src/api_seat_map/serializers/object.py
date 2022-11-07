from api_seat_map.models import Object
from rest_framework import serializers


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = "__all__"
