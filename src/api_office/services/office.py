from api_base.services import BaseService
from api_office.constants import OfficeType
from api_office.models import Department, Group, Office, Squad
from api_office.serializers.tree_office import GetDepartmentserializer, GetGroupserializer, QuerysetOfficeSerializer
from api_session.constants import WorkDayChoices
from api_session.models import Session
from api_team.models import Team, TeamMembers
from api_user.models import User
from common.constants.workday_constants import Workday
from django.db.models import F


class OfficeService(BaseService):
    @classmethod
    def import_squads(cls, squads):
        list_squads = []
        list_team_of_squad = []
        for item in squads:
            squad = Squad(name=item['squad'])
            list_squads.append(squad)
        Squad.objects.bulk_create(list_squads)

        for item in squads:
            squad = Squad.objects.filter(name=item['squad']).first()
            for team in item['teams']:
                team_name = team['team']
                team = Team.objects.filter(team_name=team_name).first()
                team.squad = squad
                list_team_of_squad.append(team)
        Team.objects.bulk_update(list_team_of_squad, ["squad"])

    @classmethod
    def import_departments(cls, departments):
        list_departments = []
        list_team_of_department = []
        for item in departments:
            department = Department(name=item['department'])
            list_departments.append(department)
        Department.objects.bulk_create(list_departments)

        for item in departments:
            department = Department.objects.filter(name=item['department']).first()
            for team in item['teams']:
                team_name = team['team']
                team = Team.objects.filter(team_name=team_name).first()
                team.department = department
                list_team_of_department.append(team)
        Team.objects.bulk_update(list_team_of_department, ["department"])

    @classmethod
    def get_office_trees(cls, group):
        group_id = group.get("id", 0)
        if not group_id:
            return

        child_groups = list(cls.get_group_query_set(group_id))
        child_offices = list(cls.get_office_query_set(group_id))

        if child_groups:
            for child_group in child_groups:
                cls.get_office_trees(child_group)
            group["children_groups"] = child_groups
        if child_offices:
            for child_office in child_offices:
                cls.get_departments(child_office)
            group["children_offices"] = child_offices

    @classmethod
    def get_departments(cls, office):
        departments = Department.objects.filter(office=office.get("id"))
        serializers = GetDepartmentserializer(departments, many=True)
        office["children_departments"] = serializers.data

    @classmethod
    def get_tree_group(cls, group):
        group_id = group.get("id", 0)
        if not group_id:
            return

        group["type"] = OfficeType.GROUP.value

        child_groups = list(cls.get_group_query_set(group_id))
        child_offices = list(cls.get_office_query_set(group_id))
        child_teams = list(cls.query_teams_by_parent_id("group", group_id))

        if child_groups:
            for child_group in child_groups:
                cls.get_tree_group(child_group)
        if child_offices:
            for child_office in child_offices:
                cls.get_tree_office(child_office)
        if child_teams:
            for child_team in child_teams:
                cls.get_tree_team(child_team)

        group["children"] = child_groups + child_offices + child_teams

    @classmethod
    def get_tree_office(cls, office):
        office_id = office.get("id", 0)
        if not office_id:
            return

        office["type"] = OfficeType.OFFICE.value
        teams = list(cls.query_teams_by_parent_id("office", office_id))
        departments = list(cls.query_departments(office_id))

        if teams:
            for team in teams:
                cls.get_tree_team(team)

        if departments:
            for department in departments:
                cls.get_tree_department(department)

        office["children"] = teams + departments
        float_users = cls.get_floating_office_users(office, teams, departments)
        if float_users:
            office["float_users"] = {
                "id": office_id,
                "data": float_users,
                "type": OfficeType.FLOATING_USERS.value,
            }

    @classmethod
    def get_tree_department(cls, department):
        department_id = department.get("id", 0)
        if not department_id:
            return
        department["type"] = OfficeType.DEPARTMENT.value
        teams = cls.query_teams_by_parent_id("department", department_id)
        if teams.exists():
            for team in teams:
                cls.get_tree_team(team)
            department["children"] = teams

    @classmethod
    def get_tree_team(cls, team):
        team_id = team.get("id", 0)
        if not team_id:
            return
        team["type"] = OfficeType.TEAM.value
        members = (
            TeamMembers.objects.filter(team=team_id)
            .exclude(member=team.get("manager_id"))
            .values(
                "id",
                "member_id",
                member_name=F("member__profile__name"),
                avatar=F("member__profile__image"),
            )
        )
        if members.exists():
            for member in members:
                member["type"] = OfficeType.MEMBER.value
            team["children"] = members

    @classmethod
    def get_group_query_set(cls, parent_group_id):
        query_set = Group.objects.filter(parent_group=parent_group_id)
        serializers = GetGroupserializer(query_set, many=True)
        return serializers.data

    @classmethod
    def get_node_group_frist(cls, parent_group_id):
        return Group.objects.filter(parent_group=parent_group_id).values(
            "id",
            "name",
            "manager_id",
            avatar=F("manager__profile__image"),
            manager_name=F("manager__profile__name"),
            manager_title=F("manager__title__title"),
        )

    @classmethod
    def get_office_query_set(cls, group_id):
        query_set = Office.objects.filter(group=group_id)
        serializers = QuerysetOfficeSerializer(query_set, many=True)
        return serializers.data

    @classmethod
    def query_teams_by_parent_id(cls, filter_field, parent_id):
        options = {filter_field: parent_id}
        if filter_field == "office":
            options["department"] = None
        if filter_field == "group":
            options["office"] = None
        return Team.objects.filter(**options).values(
            "id",
            name=F("team_name"),
            avatar=F("team_leader__profile__image"),
            manager_id=F("team_leader__id"),
            manager_name=F("team_leader__profile__name"),
        )

    @classmethod
    def query_departments(cls, office_id):
        query_set = Department.objects.filter(office=office_id)
        serializers = GetDepartmentserializer(query_set, many=True)
        return serializers.data

    @classmethod
    def create_session_for_office(cls, office):
        sessions = []
        for choice in WorkDayChoices.choices:
            dow = choice[0]

            if dow in [WorkDayChoices.SATURDAY, WorkDayChoices.SUNDAY]:
                continue

            morning_session = Session(
                start_time=Workday.DEFAULT_START_HOUR,
                end_time=Workday.DEFAULT_END_HOUR_MORNING,
                dow=dow,
                office=office,
            )
            afternoon_session = Session(
                start_time=Workday.DEFAULT_START_HOUR_AFTERNOON,
                end_time=Workday.DEFAULT_END_HOUR,
                dow=dow,
                office=office,
            )
            sessions.append(morning_session)
            sessions.append(afternoon_session)

        Session.objects.bulk_create(sessions)

    @classmethod
    def get_floating_office_users(cls, office, teams, departments):
        qs_children_teams = teams
        if departments:
            for department in departments:
                qs_children_teams += department.get("children", [])

        member_ids = []
        if qs_children_teams:
            qs_members = [
                qs_team["children"]
                for qs_team in qs_children_teams
                if qs_team.get("children") is not None
            ]

            for qs_member in qs_members:
                members = qs_member.values("member_id")
                member_ids += [member["member_id"].hex for member in members]

        office_manager_id = office.get("manager_id")
        if office_manager_id:
            member_ids.append(office_manager_id.hex)
        member_ids += [
            team.get("manager_id").hex
            for team in teams
            if team.get("manager_id") is not None
        ]
        member_ids += [
            department.get("manager_id").hex
            for department in departments
            if department.get("manager_id") is not None
        ]

        float_users = (
            User.objects.filter(profile__office=office.get("id"))
            .exclude(id__in=member_ids)
            .values("id", name=F("profile__name"), avatar=F("profile__image"))
        )
        if float_users.exists():
            for user in float_users:
                user["type"] = OfficeType.MEMBER.value
        return float_users
