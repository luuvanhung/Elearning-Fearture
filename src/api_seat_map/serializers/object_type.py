from api_seat_map.models import ObjectType
from rest_framework import serializers


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = "__all__"
