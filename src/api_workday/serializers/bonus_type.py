from api_workday.models import BonusType
from rest_framework import serializers


class BonusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusType
        fields = '__all__'
