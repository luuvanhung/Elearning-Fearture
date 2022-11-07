from api_office.models import Squad
from rest_framework import serializers


class SquadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squad
        fields = "__all__"
