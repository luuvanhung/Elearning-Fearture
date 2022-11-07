from typing import List

import requests
from api_base.services import BaseService
from api_team.models import Team, TeamMembers
from api_user.models import Profile, User
from api_user.serializers.profile import TeamProfile
from api_user.services import UserService
from common.constants.user_constants import TitleConstant
from django.conf import settings
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate


class TeamService(BaseService):
    # get all members of a team
    @classmethod
    def get_members_in_team(cls, team_id):
        return list(
            TeamMembers.objects.filter(team_id=team_id).values_list(
                "member_id", flat=True
            )
        )

    @classmethod
    def import_teams(cls, teams):
        list_teams = []
        list_team_members = []
        for item in teams:
            team_name = item.get("team")
            team = Team(team_name=team_name)
            list_teams.append(team)
        Team.objects.bulk_create(list_teams)

        for item in teams:
            team_name = item.get("team")
            team = Team.objects.filter(team_name=team_name).first()
            members = item.get("members")
            for member in members:
                member_email = member.get("email")
                user = UserService.get_user_by_email(member_email)
                if user and team:
                    list_team_members.append(TeamMembers(member=user, team=team))
        if list_team_members:
            TeamMembers.objects.bulk_create(list_team_members)

    @classmethod
    def update_line_manager_in_team(cls, team):
        leader = team.team_leader
        if leader:
            team_members = TeamMembers.objects.filter(team_id=team.id)
            for team_member in team_members:
                member = team_member.member
                if member.profile.line_manager != leader.profile:
                    member.profile.line_manager = leader.profile
                    member.profile.teams = team.team_name
                    member.profile.office = team.office
                    member.profile.save()

    # check this user has a team or not
    @classmethod
    def check_had_team(cls, user_id):
        return bool(TeamMembers.objects.filter(member_id=user_id).first())

    @classmethod
    def check_in_team(cls, user, team_id):
        return bool(TeamMembers.objects.filter(team_id=team_id, member=user).first())

    # check whether pm has team or not
    @classmethod
    def check_owner_team(cls, user, team_id):
        if user.staff:
            return True
        return Team.objects.filter(id=team_id, team_leader_id=user.id)

    # get team of current user
    @classmethod
    def get_team(cls, user_id):
        return list(
            TeamMembers.objects.filter(member_id=user_id).values_list(
                "team_id", flat=True
            )
        )

    @classmethod
    def add_new_member(cls, instance, **kwargs):
        user = UserService.get_user_by_email(kwargs.get("email"))
        if user:
            cls.update_user_team(user, instance.id)

    @classmethod
    def remove_member(cls, data, instance):
        user = UserService.get_user_by_email(data.get("email"))
        if user:
            cls._remove_user_team(user, instance.id)
            user.profile.save()

    @classmethod
    def delete_team(cls, team: Team):
        Profile.objects.filter(teams=team.team_name).update(teams="", line_manager=None)
        TeamMembers.objects.filter(team_id=team.id).delete()

    @classmethod
    def get_leader(cls, text=None, limit=10):
        if text is None:
            text = ""
        users = (
            User.objects.select_related("profile")
            .filter(profile__name__istartswith=text, staff=0)
            .exclude(title__title=TitleConstant.PROJECT_MANAGER)
            .select_related("leader")
            .filter(leader__team_leader__isnull=True)[:limit]
        )
        return [
            {"id": user.id, "email": user.email, "name": user.profile.name}
            for user in users
        ]

    @classmethod
    def get_potential_members(cls):
        profiles = (
            Profile.objects.select_related("user")
            .filter(user__active=1)
            .exclude(Q(user__staff=True))
        )
        return [
            {"id": profile.user.id, "name": profile.name, "email": profile.user.email}
            for profile in profiles
            if not cls.check_had_team(profile.user.id)
        ]

    @classmethod
    def modify_members(cls, team, member_ids):
        existed_members = TeamMembers.objects.filter(team=team.id)
        team_leader = Team.objects.filter(id=team.id).first().team_leader
        if not member_ids:
            existed_members.delete()

        existed_members = existed_members.all()
        member_ids = {str_id.replace("-", "") for str_id in member_ids.split(",")}
        deleted_ids = set()
        stable_ids = set()

        for existed_member in existed_members:
            str_id = str(existed_member.member.id).replace("-", "")
            if str_id not in member_ids:
                deleted_ids.add(str_id)
            else:
                stable_ids.add(str_id)
        existed_members.filter(member__in=deleted_ids).exclude(
            member=team_leader.id.hex
        ).delete()
        for deleted_id in deleted_ids:
            deleted_user = User.objects.get(id=deleted_id)
            Profile.objects.filter(user=deleted_user).update(teams="")

        added_ids = member_ids - (deleted_ids.union(stable_ids))
        added_objects = []
        for added_id in added_ids:
            added_objects.append(TeamMembers(team_id=team.id, member_id=added_id))
            added_user = User.objects.filter(id=added_id).first()
            if added_user and team.team_leader and team.team_leader != added_user:
                added_user.profile.line_manager = team.team_leader.profile
                added_user.profile.teams = team.team_name
                added_user.profile.office = team.office
                added_user.profile.save()
        TeamMembers.objects.bulk_create(added_objects)

    @classmethod
    def get_profile(cls, data, instance, leaders):
        check = True
        data.update(leader_name="No leader")
        if data.get("team_leader"):
            for leader in leaders:
                if cls.leader_accept(data, leader):
                    data.update(leader_name=leader.get("name", "No leader"))
                    check = False
                    break
        if check:
            data.update(team_leader=None)
        team_member_ids = cls.get_members_in_team(instance.pk)
        profiles = Profile.objects.filter(user_id__in=team_member_ids)
        for profile in profiles:
            profile.team_leader_id = data.get("team_leader")
        data.update(
            employee_number=profiles.count(),
            employee_list=TeamProfile(profiles, many=True).data,
        )
        return data

    @classmethod
    def leader_accept(cls, data, leader):
        return (
            data.get("team_leader") == leader.get("user_id")
            and leader.get("user__active")
            # and cls.check_in_team(leader.get("user_id"), data.get("id"))
        )

    @classmethod
    def update_leader_team(cls, leader, team_id):
        team = Team.objects.get(pk=team_id)
        if not cls.check_had_team(leader.id) and team:
            TeamMembers.objects.create(member=leader, team=team)

    @classmethod
    def update_user_team(cls, user, team_id):
        team = Team.objects.get(pk=team_id)
        if not cls.check_had_team(user.id):
            if not cls.check_in_team(user, team_id):
                TeamMembers.objects.create(member=user, team=team)
        else:
            TeamMembers.objects.filter(member=user).update(team=team)
        if team.team_leader and team.team_leader != user:
            user.profile.line_manager = team.team_leader.profile
            user.profile.teams = team.team_name
            user.profile.office = team.office
            user.profile.save()

    @classmethod
    def _remove_user_team(cls, member, team_id):
        TeamMembers.objects.filter(member_id=member.id, team_id=team_id).delete()
        users = User.objects.get(pk=member.id)
        Profile.objects.filter(user=users).update(teams="")

    @classmethod
    def set_leader(cls, team, **kwargs):
        email = kwargs.get("email")
        user = UserService.get_user_by_email(email)
        if user:
            team.team_leader = user
            team.save()
            cls.update_line_manager_in_team(team)
            cls.update_user_team(user, team.id)

    @classmethod
    def move_team(cls, user_id, current_team_id, new_team_id):
        user = User.objects.get(id=user_id)
        cls._remove_user_team(user, current_team_id)
        cls.update_user_team(user, new_team_id)

    @classmethod
    def get_filter_query(cls, request):
        key_words = request.query_params.get("key")
        if key_words:
            key_words = Collate(Value(key_words.strip()), "utf8mb4_general_ci")

        queryset = Team.objects.filter(Q(team_name__icontains=key_words)
                                       | Q(team_email__icontains=key_words))
        return queryset

    @classmethod
    def destroy_multi_teams(cls, team_ids: List[str]) -> bool:
        try:
            with transaction.atomic():
                teams = Team.objects.filter(id__in=team_ids)
                for team in teams:
                    TeamService.delete_team(team=team)
                teams.delete()
            return True
        except Exception as e:
            return False

    @classmethod
    def get_slack_id_by_email(cls, list_email: List[str]) -> dict:
        dict_email = {}
        token = settings.SLACK_BOT_USER_OAUTH_TOKEN
        my_headers = {'Authorization': f"Bearer {token}"}
        users_list = requests.get('https://slack.com/api/users.list', headers=my_headers).json()
        members = users_list['members']
        for email in list_email:
            for user in members:
                if user.get('profile'):
                    user_profile = user.get('profile')
                    if not user.get('deleted', True) and user_profile.get('email', False) == email:
                        dict_email[email] = user.get('id', '')
        return dict_email

    @classmethod
    def get_teams_of_user(cls, user_id: str) -> List[dict]:
        teams = Team.objects.filter(Q(team__member=user_id) | Q(team_leader=user_id)).values(
            "id", "team_name", "team_leader").distinct()
        data = []
        members = Profile.objects.filter(
            Q(user__member__team_id__in=[team.get("id") for team in teams]) |
            Q(user_id__in=[team.get("team_leader") for team in teams])
        ).prefetch_related("user__member__team").values("id", "name", "user_id", "user__member__team")
        for team in teams:
            team_members = [
                member
                for member in members
                if member.get("user__member__team") == team.get("id") or member.get("user_id") == team.get("team_leader")
            ]
            data.append({
                "id": team.get("id"),
                "team_name": team.get("team_name"),
                "team_leader": team.get("team_leader"),
                "members": team_members,
            })
        return data
