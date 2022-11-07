import threading

from api_base.services import GoogleCalendar
from common.constants.google_constants import EventCalendarConstant
from core.settings.base import CALENDAR_ID


class EventGoogle(threading.Thread):
    def __init__(self, calendarId=None, eventId=None, body=None, event_type=None):
        self.calendarId = calendarId
        self.eventId = eventId
        self.body = body
        self.event_type = event_type

    def run(self):
        try:
            service = GoogleCalendar.get_calendar_service()
            if self.event_type == EventCalendarConstant.UPDATE:
                service.events().update(
                    calendarId=CALENDAR_ID,
                    eventId=self.eventId,
                    body=self.body,
                ).execute()
            if self.event_type == EventCalendarConstant.DELETE:
                service.events().delete(
                    calendarId=CALENDAR_ID,
                    eventId=self.eventId,
                ).execute()
            if self.event_type == EventCalendarConstant.INSERT:
                service.events().insert(
                    calendarId=CALENDAR_ID,
                    body=self.body,
                ).execute()
        except Exception as e:
            print(str(e))


class SendGoogleEvent:
    @staticmethod
    def start(calendarId, eventId, event, event_type):
        EventGoogle(
            calendarId=calendarId, eventId=eventId, body=event, event_type=event_type
        ).start()
