from api_skill.models import TitleSkill
from api_user.models import Titles
from django.db.models import F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class TitleSkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = ("id", "title")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        title_id = data["id"]
        title_skills = TitleSkill.objects.filter(title=title_id).values(
            "id",
            "skill_definition",
            skill_id=F("skill_definition__skill"),
            skill_name=F("skill_definition__skill__name"),
            level_id=F("skill_definition__level"),
            level_name=F("skill_definition__level__name"),
            set_by_user_name=F("set_by_user__profile__name"),
        )
        data["title_skills"] = list(title_skills)

        return data


class TitleSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleSkill
        fields = "__all__"

    def validate(self, attrs):
        title = attrs.get("title", None)
        skill_definition = attrs.get("skill_definition", None)

        if not title:
            raise ValidationError({"details": "title empty"})
        if not skill_definition:
            raise ValidationError({"details": "skill_definition empty"})

        request = self.context.get("request")
        user = request.user
        attrs["set_by_user"] = user

        instance_id = None
        if self.instance:
            instance_id = self.instance.id
        qs = TitleSkill.objects.filter(
            title=title.id, skill_definition__skill_id=skill_definition.skill_id
        ).exclude(id=instance_id)
        if qs.exists():
            raise ValidationError(
                {"details": "One title just have one skill in skill definition"}
            )

        return attrs
