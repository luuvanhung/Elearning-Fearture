from api_base.services import BaseService
from api_wfh.models.wfh_date import WfhDate
from api_wfh.serializers.calendar import WfhDateForCalendarSerializer


class CalendarServices(BaseService):
    @classmethod
    def get_days_wfh(cls, user):
        wfh_days = WfhDate.objects.filter(wfh_request__user=user)
        list_dates = WfhDateForCalendarSerializer(wfh_days, many=True).data
        data = [
            {
                "id": wfh_date.get("id"),
                "date": wfh_date.get("date"),
                "wfh_request": wfh_date.get("wfh_request"),
                "name": user.profile.name,
                "email": user.email,
                "lunch": wfh_date.get("lunch"),
            }
            for wfh_date in list_dates
        ]
        return data
