from api_base.services import BaseService
from api_office.models import Group
from rest_framework.exceptions import ValidationError


class GroupService(BaseService):
    @classmethod
    def update(cls, instance, validated_data):
        updated_parent_group = validated_data.get("parent_group", 0)
        if updated_parent_group:
            parent_group_id = updated_parent_group.id
            while True:
                parent_group_obj = Group.objects.filter(id=parent_group_id).first()
                if not parent_group_obj:
                    raise ValidationError(
                        {"details": "parent group value is not valid"}
                    )
                if parent_group_obj.parent_group_id == instance.id:
                    raise ValidationError(
                        {
                            "details": "this parent group value will make a ring of groups, it's not valid"
                        }
                    )
                if not parent_group_obj.parent_group:
                    break
                parent_group_id = parent_group_obj.parent_group_id

        return validated_data
