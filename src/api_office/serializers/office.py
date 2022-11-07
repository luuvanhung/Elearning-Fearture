from api_office.models import Office
from api_office.services import OfficeService
from rest_framework import serializers


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        office = super().create(validated_data)
        OfficeService.create_session_for_office(office)
        return office
