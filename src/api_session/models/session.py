from api_base.models import TimeStampedModel
from api_office.models import Office
from api_session.constants import WorkDayChoices
from django.db import models


class Session(TimeStampedModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    dow = models.IntegerField(choices=WorkDayChoices.choices)
    office = models.ForeignKey(
        Office, related_name="sessions", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "hr_sessions"
