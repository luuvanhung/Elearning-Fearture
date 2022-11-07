from api_base.models import TimeStampedModel
from api_team.models import Team
from api_user.models import User
from django.db import models


class TeamMembers(TimeStampedModel):
    member = models.ForeignKey(User, related_name="member", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="team", on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_team_members"
