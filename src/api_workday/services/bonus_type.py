from api_base.services import BaseService
from api_workday.models import BonusLeave, BonusType
from api_workday.services import BonusLeaveService
from django.db import transaction


class BonusTypeService(BaseService):
    @classmethod
    def delete(cls, bonus_type: BonusType) -> bool:
        try:
            with transaction.atomic():
                bonus_leaves = BonusLeave.objects.filter(bonus_type=bonus_type)
                for bonus_leave in bonus_leaves:
                    destroy_leave = -bonus_leave.bonus_days
                    BonusLeaveService.add_bonus_days_current_days_off([bonus_leave.profile.id], destroy_leave)
                    bonus_leave.delete()
                bonus_type.delete()
            return True
        except Exception as e:
            return False
