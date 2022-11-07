import logging

from api_base.services import BaseService
from api_skill.models import Skill, SkillDefinition, SkillLevel
from rest_framework.exceptions import ValidationError


class SkillDefinitionService(BaseService):
    @classmethod
    def delete_by_skill_id(cls, skill_id):
        try:
            SkillDefinition.objects.filter(skill_id=skill_id).delete()
        except Exception as e:
            logging.exception(e)
            return False
        return True

    @classmethod
    def create(cls, validated_data):
        skill_name = validated_data.get("skill", {}).get("name", "").strip()
        level_id = validated_data.get("level", {}).get("id", 0)

        if not skill_name:
            raise ValidationError({"detail": "Skill name is empty"})
        if not level_id:
            raise ValidationError({"detail": "Level id is empty"})

        skill = Skill.objects.get_or_create(name=skill_name)[0]
        validated_data["skill"]["id"] = skill.id

        if SkillDefinition.objects.filter(skill=skill.id, level=level_id).exists():
            raise ValidationError(
                {"detail": "Existed another record contains this skill_id and level_id"}
            )

        validated_data["skill"] = Skill(**validated_data["skill"])
        validated_data["level"] = SkillLevel(**validated_data["level"])
        return validated_data

    @classmethod
    def update(cls, instance, validated_data):
        skill_id = validated_data.get("skill", {}).get("id", 0)
        level_id = validated_data.get("level", {}).get("id", 0)

        if not skill_id:
            raise ValidationError({"detail": "Skill id is empty"})
        if not level_id:
            raise ValidationError({"detail": "Level id is empty"})
        if not Skill.objects.filter(id=skill_id).exists():
            raise ValidationError({"detail": "Skill id does not existed"})

        skill_id = instance.skill_id if not skill_id else skill_id
        level_id = instance.level_id if not level_id else level_id
        if (
            SkillDefinition.objects.filter(skill_id=skill_id, level_id=level_id)
            .exclude(id=instance.id)
            .exists()
        ):
            raise ValidationError(
                {"detail": "Existed another record contains this skill_id and level_id"}
            )

        validated_data["skill"] = Skill(**validated_data.get("skill"))
        validated_data["level"] = SkillLevel(**validated_data.get("level"))
        return validated_data
