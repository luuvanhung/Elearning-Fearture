from api_lunch.models import Lunch
from rest_framework import serializers


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["name_provider"] = instance.provider.name if instance.provider else ""
        return ret
