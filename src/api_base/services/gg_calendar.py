import datetime

import httplib2
from common.constants.workday_constants import Workday
from core.settings.base import CALENDAR_ID, TIME_ZONE
from django.conf import settings
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleCalendar:
    CLIENT_SECRET_FILE = "api/credentials.json"
    SCOPES = "https://www.googleapis.com/auth/calendar"
    scopes = [SCOPES]

    @classmethod
    def get_calendar_service(cls):
        """
        Get calendar service from google calendar
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cls.CLIENT_SECRET_FILE, cls.SCOPES
        )
        http = credentials.authorize(httplib2.Http())
        service = build("calendar", "v3", http=http, cache_discovery=False)
        return service

    @classmethod
    def create_leave_event(cls, request_off, user_team):
        """
        Create google calendar event
        @param request_off: request_off
        @param user_team: team of user
        """
        date_offs = request_off.date_off.all()
        service = cls.get_calendar_service()
        reason = request_off.reason
        team_name = start = end = ""
        if user_team is not None:
            team_name = user_team.team_name
        for date_off in date_offs:
            title = f"{request_off.profile.name} - {team_name} - {date_off.type}"
            date = date_off.date
            if date_off.type != "All day":
                start = datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    int(date_off.type[0:2]),
                    int(date_off.type[3:5]),
                ).isoformat()
                end = datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    int(date_off.type[6:8]),
                    int(date_off.type[9:11]),
                ).isoformat()
            elif date_off.type == "All day":
                start = datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    int(Workday.DEFAULT_START_HOUR[0:2]),
                    int(Workday.DEFAULT_START_HOUR[3:5]),
                ).isoformat()
                end = datetime.datetime(
                    date.year,
                    date.month,
                    date.day,
                    int(Workday.DEFAULT_END_HOUR[0:2]),
                    int(Workday.DEFAULT_END_HOUR[3:5]),
                ).isoformat()
            service.events().insert(
                calendarId=CALENDAR_ID,
                body={
                    "summary": title,
                    "description": f"Reason: {reason}",
                    "start": {"dateTime": start, "timeZone": TIME_ZONE},
                    "end": {"dateTime": end, "timeZone": TIME_ZONE},
                },
            ).execute()
        return False

    @classmethod
    def sync_leave_event(
        cls, reason=None, name=None, type=None, team_name=None, date=None
    ):
        service = cls.get_calendar_service()
        reason = reason
        team_name = start = end = ""
        if team_name is not None:
            team_name = team_name
        title = f"{name} - {team_name} - {type}"
        if type != "All day":
            start = datetime.datetime(
                date.year,
                date.month,
                date.day,
                int(type[0:2]),
                int(type[3:5]),
            ).isoformat()
            end = datetime.datetime(
                date.year,
                date.month,
                date.day,
                int(type[6:8]),
                int(type[9:11]),
            ).isoformat()
        elif type == "All day":
            start = datetime.datetime(
                date.year,
                date.month,
                date.day,
                int(Workday.DEFAULT_START_HOUR[0:2]),
                int(Workday.DEFAULT_START_HOUR[3:5]),
            ).isoformat()
            end = datetime.datetime(
                date.year,
                date.month,
                date.day,
                int(Workday.DEFAULT_END_HOUR[0:2]),
                int(Workday.DEFAULT_END_HOUR[3:5]),
            ).isoformat()
        try:
            service.events().insert(
                calendarId=CALENDAR_ID,
                body={
                    "summary": title,
                    "description": f"Reason: {reason}",
                    "start": {"dateTime": start, "timeZone": TIME_ZONE},
                    "end": {"dateTime": end, "timeZone": TIME_ZONE},
                },
            ).execute()
        except Exception as e:
            print(e)

    @classmethod
    def create_holiday_event(cls, data):
        service = cls.get_calendar_service()
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        event = {
            "summary": str(data.get("office").name + ": " + data.get("title")),
            "description": f'Reason: {str(data.get("descriptions"))}',
            "start": {"date": str(start_date), "timeZone": TIME_ZONE},
            "end": {"date": str(end_date), "timeZone": TIME_ZONE},
        }
        if data["repeat"]:
            event["recurrence"] = []
            event["recurrence"].append(
                f'RRULE:FREQ=YEARLY;COUNT={str(data.get("count"))}'
            )

        result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        if result:
            return result
        return False

    @classmethod
    def delete_holiday_event(cls, data):
        service = cls.get_calendar_service()
        try:
            for element in data:
                service.events().delete(
                    calendarId=CALENDAR_ID,
                    eventId=element.calendar_id,
                ).execute()
        except Exception:
            raise Exception("Failed to delete holiday event")

    @classmethod
    def update_holiday_event(cls, data, new_data):
        service = cls.get_calendar_service()
        start_date = new_data.get("start_date")
        end_date = new_data.get("end_date")
        event = {
            "summary": str(new_data.get("office").name + ": " + new_data.get("title")),
            "description": f'Reason: {str(new_data.get("descriptions"))}',
            "start": {"date": str(start_date), "timeZone": TIME_ZONE},
            "end": {"date": str(end_date), "timeZone": TIME_ZONE},
        }
        if new_data["repeat"]:
            event["recurrence"] = []
            event["recurrence"].append(
                f'RRULE:FREQ=YEARLY;COUNT={str(new_data.get("count"))}'
            )

        result = (
            service.events()
            .update(
                calendarId=CALENDAR_ID,
                eventId=str(data.calendar_id),
                body=event,
            )
            .execute()
        )
        if result:
            return result
        return False

    @classmethod
    def get_all_event(cls, time_start=None, time_end=None):
        service = cls.get_calendar_service()  # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                singleEvents=True,
                orderBy="startTime",
                timeMin=time_start,
                timeMax=time_end,
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    @classmethod
    def get_event_search(cls, team_name):
        """
        Search data in Google Calendar with parameters q
        @param team_name: name of team you want to search
        """
        service = cls.get_calendar_service()
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                singleEvents=True,
                orderBy="startTime",
                alwaysIncludeEmail=True,
                q=team_name,
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    @classmethod
    def get_event_from_now(cls):
        service = cls.get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    @classmethod
    def update_event(cls, data, old_content, new_content, user_team):
        # update the event to according time
        service = cls.get_calendar_service()
        title = f"{data.get('title')} - {user_team} - {new_content}"
        reason = "No reason"
        if data.get("reason"):
            reason = data.get("reason")
        start = str(data.get("date")) + "T" + new_content.split(" ")[-3][1:6] + ":00"
        end = str(data.get("date")) + "T" + new_content.split(" ")[-1][:5] + ":00"

        calendar_id = None
        items = cls.get_event_from_now()
        for item in items:
            if item.get(
                "summary"
            ) == f"{data.get('title')} - {user_team} - {old_content}" and item.get(
                "start"
            ).get(
                "dateTime"
            )[
                :10
            ] == data.get(
                "start"
            ):
                calendar_id = item.get("id")
        if calendar_id:
            service.events().update(
                calendarId=CALENDAR_ID,
                eventId=calendar_id,
                body={
                    "summary": title,
                    "description": f"Reason: {reason}",
                    "start": {"dateTime": start, "timeZone": TIME_ZONE},
                    "end": {"dateTime": end, "timeZone": TIME_ZONE},
                },
            ).execute()

    @classmethod
    def delete_event(cls, items, dates, user_team):
        service = cls.get_calendar_service()
        try:
            calendar_id = None
            for date in dates:
                for item in items:
                    if item.get(
                        "summary"
                    ) == f"{date.title} - {user_team} - {date.content}" and item.get(
                        "start"
                    ).get(
                        "dateTime"
                    )[
                        :10
                    ] == str(
                        date.date
                    ):
                        calendar_id = item.get("id")
                if calendar_id:
                    service.events().delete(
                        calendarId=CALENDAR_ID,
                        eventId=calendar_id,
                    ).execute()
                    calendar_id = None
        except Exception:
            raise Exception("Failed to delete event")

    @classmethod
    def create_probation_reminders(
        cls,
        remind_probation,
        probation_end_date,
        reminder_date,
    ):
        try:
            service = cls.get_calendar_service()
            title = f"Evaluation Reminder - {remind_probation.get('employee').get('profile').get('name')}"
            event = {
                "summary": title,
                "description": f"This evaluation ends on {probation_end_date}",
                "start": {"date": str(reminder_date), "timeZone": TIME_ZONE},
                "end": {"date": str(reminder_date), "timeZone": TIME_ZONE},
            }
            if settings.USE_INVITE_ATTENDEES_GOOGLE:
                event["attendees"] = [
                    {"email": item.get("personal_email")}
                    for item in remind_probation.get("reminder_user")
                ]

            result = (
                service.events()
                .insert(calendarId=CALENDAR_ID, sendNotifications=True, body=event)
                .execute()
            )
            if result:
                return result
            return False
        except Exception:
            raise Exception("Failed to create reminder event")

    @classmethod
    def delete_reminder_event(cls, reminders):
        service = cls.get_calendar_service()
        try:
            for reminder in reminders:
                calendar_id = reminder.calendar_id
                if calendar_id:
                    service.events().delete(
                        calendarId=CALENDAR_ID,
                        eventId=calendar_id,
                    ).execute()
        except Exception:
            raise Exception("Failed to delete reminder event")

    @classmethod
    def update_reminder_event(
        cls,
        calendar_id,
        remind_probation,
        probation_end_date,
        reminder_date,
    ):
        service = cls.get_calendar_service()
        try:
            title = f"Evaluation Reminder - {remind_probation.get('employee').get('profile').get('name')}"
            event = {
                "summary": title,
                "description": f"This evaluation ends on {probation_end_date}",
                "start": {"date": str(reminder_date), "timeZone": TIME_ZONE},
                "end": {"date": str(reminder_date), "timeZone": TIME_ZONE},
            }
            if settings.USE_INVITE_ATTENDEES_GOOGLE:
                event["attendees"] = [
                    {"email": item.get("personal_email")}
                    for item in remind_probation.get("reminder_user")
                ]
            if calendar_id:
                service.events().update(
                    calendarId=CALENDAR_ID,
                    eventId=calendar_id,
                    body=event,
                ).execute()
        except Exception:
            raise Exception("Failed to update reminder event")
