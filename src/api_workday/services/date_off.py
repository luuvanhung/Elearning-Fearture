from api_base.services import BaseService
from api_workday.models import DateOff
from common.constants.workday_constants import Workday


class DateOffService(BaseService):
    @classmethod
    def get_num_days_off_by_list_date(cls, list_date_off):
        date_leave = 0
        for date_off in list_date_off:
            if date_off.type == Workday.FULL:
                date_leave += 1
            else:
                date_leave += 0.5
        return date_leave

    @classmethod
    def get_num_days_off(cls, request_off):
        list_date_off = DateOff.objects.filter(request_off_id=request_off.id)
        return cls.get_num_days_off_by_list_date(list_date_off)
