from api_base.views import BaseViewSet
from api_team.models import Team
from api_user.models import Profile
from api_workday.services.statistic import StatisticServices
from common.constants.api_constants.http_method import HttpMethod
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class StatisticDateOffView(BaseViewSet):
    required_alternate_scopes = {
        "user": [["statistic_dateoff:user"]],
        "team": [["statistic_dateoff:team"]],
        "office": [["statistic_dateoff:office"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def user(self, request):
        profile = Profile.objects.get(id=request.user.profile.id)
        year = request.query_params.get("y")
        data = StatisticServices.get_date_off_for_statistic_user_dynamic(year, profile)
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def office(self, request):
        profiles = Profile.objects.all()
        data = StatisticServices.get_date_off_for_statistic_admin_dynamic(
            profiles=profiles,
            filters=request.query_params
        )
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)

    @action(methods=[HttpMethod.GET], detail=False)
    def team(self, request):
        team = Team.objects.filter(team_name=request.query_params.get("team")).first()
        if team:
            profile_teams = Profile.objects.filter(
                Q(user__member__team=team.id) | Q(id=request.query_params.get("profile")) | Q(user_id=team.team_leader)
            )
            data = StatisticServices.get_date_off_for_statistic_admin_dynamic(
                profiles=profile_teams,
                filters=request.query_params
            )
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Don't have team to report"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def team_all_year(self, request):
        year = request.query_params.get("y")
        profile_id = request.query_params.get("p")
        profile = Profile.objects.get(pk=profile_id)
        profile_teams = Profile.objects.filter(teams=profile.teams)
        data = StatisticServices.get_total_date_off_year_by_team(
            year=year, profiles=profile_teams
        )
        return Response(data, status=status.HTTP_200_OK)
