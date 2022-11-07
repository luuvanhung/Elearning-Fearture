from api_session.models import Session
from api_session.services import SessionService
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"

    def validate(self, attrs):
        start_time = attrs.get("start_time", None)
        end_time = attrs.get("end_time", None)
        dow = attrs.get("dow", None)
        office = attrs.get("office", None)

        if not (start_time and end_time):
            raise ValidationError({"detail": "start_time/end_time is missing"})
        if start_time >= end_time:
            raise ValidationError({"detail": "start_time must before end_time"})
        if dow is None:
            raise ValidationError({"detail": "dow is missing"})
        if office is None:
            raise ValidationError({"detail": "office is missing"})

        return attrs

    def create(self, validated_data):
        SessionService.check_overlapping(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        SessionService.check_overlapping(validated_data, instance.id)
        return super().update(instance, validated_data)
