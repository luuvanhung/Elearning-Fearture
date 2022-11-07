from api_base.services import BaseService
from api_skill.models import SkillTarget


class SkillTargetService(BaseService):
    @classmethod
    def is_valid(cls, validated_data, exclude_id=None):
        target_user = validated_data.get("target_user")
        skill_definition = validated_data.get("skill_definition")
        error_message = ""

        if validated_data.get("target_user") == validated_data.get("set_by_user"):
            error_message = "You cannot set target skill by yourself"

        skill_target = SkillTarget.objects.filter(
            target_user=target_user, skill_definition__skill=skill_definition.skill
        ).exclude(id=exclude_id)
        if skill_target.exists():
            error_message = (
                "One user cannot have two skill target record with same skill field"
            )
        return error_message

    @classmethod
    def delete_record(cls, access_user, record_id):
        skill_target = SkillTarget.objects.filter(id=record_id).first()
        if skill_target:
            if skill_target.set_by_user != access_user:
                return False
            else:
                skill_target.delete()
                return True
        return False
