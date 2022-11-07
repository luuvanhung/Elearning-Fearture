from api_base.services import BaseService, GoogleCalendar


class HolidayService(BaseService):
    @classmethod
    def create_event(cls, data):
        try:
            if not data.get("calendar_id"):
                result = GoogleCalendar.create_holiday_event(data)
                return result
            else:
                return data

        except Exception:
            raise Exception("Error")

    @classmethod
    def update_event(cls, data, new_data):
        result = GoogleCalendar.update_holiday_event(data, new_data)
        return result

    @classmethod
    def delete_event(cls, data):
        try:
            GoogleCalendar.delete_holiday_event(data)
        except Exception:
            Exception("CalendarId not found")
