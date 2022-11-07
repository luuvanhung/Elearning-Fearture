from api_office.serializers import DepartmentSerializer, GroupSerializer, OfficeSerializer
from api_team.models import Team
from api_team.services import TeamService
from api_user.models import Profile
from rest_framework import serializers


class TeamSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        TeamService.update_leader_team(validated_data.get("team_leader"), team.id)
        return team

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.group:
            ret["group_name"] = instance.group.name
        if instance.office:
            ret["office_name"] = instance.office.name
        if instance.department:
            ret["department_name"] = instance.department.name
        if instance.squad:
            ret["squad_name"] = instance.squad.name
        leaders = (
            Profile.objects.select_related("user")
            .filter(user_id=instance.team_leader)
            .values("user_id", "user__active", "teams", "name")
        )
        ret = TeamService.get_profile(ret, instance, leaders)
        return ret

    class Meta:
        model = Team
        fields = "__all__"


class TeamDetailsSerializers(serializers.ModelSerializer):
    group = GroupSerializer()
    office = OfficeSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Team
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        leaders = (
            Profile.objects.select_related("user")
            .filter(user_id=instance.team_leader)
            .values("user_id", "user__active", "teams", "name")
        )
        ret = TeamService.get_profile(ret, instance, leaders)
        return ret


class MemberSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField(max_length=255)
