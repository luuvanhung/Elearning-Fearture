import datetime

from api_team.models import Team
from api_user.models import Profile, User
from api_user.serializers import PhotoSerializer
from django.conf import settings
from rest_framework import serializers

from ..serializers.title import TitleSerializer


class ProfileSerializers(serializers.ModelSerializer):
    admin = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    title = TitleSerializer(many=True, required=False)
    line_manager_email = serializers.EmailField(required=False)
    line_manager_user_id = serializers.EmailField(required=False)
    photo = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.update(active=instance.user.active)
        # restrict access to other profile

        # Get line manager email
        manager = User.objects.filter(profile__id=ret.get("line_manager")).first()
        if manager:
            ret.update(line_manager_email=manager.email)
            ret.update(line_manager_user_id=manager.id)
            ret.update(line_manager_user_name=manager.profile.name)
        # Get team for each user
        teams = []
        team_queryset = Team.objects.filter(
            team__member=instance.user.id
        ).select_related()
        if team_queryset:
            for team in team_queryset:
                teams.append({"id": team.id, "name": team and team.team_name or ""})
        ret.update(teams=teams)
        return ret

    def update(self, instance, validated_data):
        profile = super().update(instance, validated_data)
        email = validated_data.get("email")
        admin = validated_data.get("admin")
        titles = validated_data.get("title")
        join_date = validated_data.get("join_date")
        birth_date = validated_data.get("birth_day")
        if birth_date and birth_date > datetime.date.today():
            raise serializers.ValidationError({"error": "Birthday cannot be in the future!"})
        if join_date and join_date > datetime.date.today():
            raise serializers.ValidationError({"error": "Join date cannot be in the future!"})
        if titles:
            list_id_title = [title.get("id") for title in titles]
            profile.user.title.set(list_id_title)
        else:
            profile.user.title.clear()
        request = self.context.get("request")
        if request:
            access_user = request.user
            if email:
                if access_user.is_admin:
                    if admin == "true":
                        profile.user.staff = True
                    else:
                        profile.user.staff = False
                profile.user.email = email
                profile.user.save()
        return profile


class ProfileInlineSerializers(serializers.ModelSerializer):
    title = TitleSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'name',
            'personal_email',
            'teams',
            'office',
            'image',
            'title'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Get team for each user
        teams = Team.objects.filter(
            team__member=instance.user.id
        ).values('id', 'team_name')
        ret.update(teams=teams)
        return ret


class ProfileAvatar(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("image",)


class ProfileSlackId(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "slack_id",
        )


class ProfileLunch(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "veggie")


class TeamProfile(serializers.ModelSerializer):
    team_leader_id = serializers.UUIDField(required=False)

    class Meta:
        model = Profile
        fields = ("id", "name", "phone", "team_leader_id", "user")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get("image"):
            ret.update(image=settings.MEDIA_IMAGE + ret.get("image"))
        role = "Member"
        if ret.get("user") and ret.get("user") == instance.team_leader_id:
            role = "Leader"
        ret.update(title=role, email=instance.user.email)
        return ret
