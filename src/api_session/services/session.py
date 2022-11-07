from api_base.services import BaseService
from api_session.models import Session
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class SessionService(BaseService):
    @classmethod
    def check_overlapping(cls, validated_data, session_id=None):
        start_time = validated_data.get("start_time")
        end_time = validated_data.get("end_time")
        dow = validated_data.get("dow")
        office = validated_data.get("office")

        overlapping_sessions = Session.objects.exclude(id=session_id).filter(
            Q(dow=dow),
            Q(office=office),
            Q(start_time__gte=start_time, start_time__lt=end_time)
            | Q(start_time__lt=start_time, end_time__gt=start_time),
        )
        if overlapping_sessions.exists():
            raise ValidationError({"detail": "time range is overlapping"})
