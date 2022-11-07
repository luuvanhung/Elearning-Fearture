from api_base.models import TimeStampedModel
from api_office.models import Department, Group, Office, Squad
from api_user.models import User
from django.db import models


class Team(TimeStampedModel):
    team_name = models.CharField(max_length=255, unique=True)
    team_email = models.EmailField(max_length=255, blank=True, null=True)
    team_leader = models.ForeignKey(
        User, related_name="leader", on_delete=models.SET_NULL, blank=True, null=True
    )
    slack_channel = models.CharField(max_length=255, default="", blank=True)
    office = models.ForeignKey(
        Office, related_name="team", on_delete=models.CASCADE, null=True, blank=True
    )
    group = models.ForeignKey(
        Group, related_name="team", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, related_name="team", on_delete=models.CASCADE, null=True, blank=True
    )
    squad = models.ForeignKey(
        Squad, related_name = "team", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "hr_teams"
