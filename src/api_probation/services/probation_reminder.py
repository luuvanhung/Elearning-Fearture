from datetime import datetime

from api_base.services import BaseService, GoogleCalendar, SlackResponseService
from api_probation.models import Probation, ProbationReminder
from api_probation.serializers.probation import ProbationReminderUserSerializer
from api_slackbot.services.slack.response import SubComponentBuilder


class ProbationReminderService(BaseService):
    @classmethod
    def create(cls, probation_reminders, probation_id):
        probation = Probation.objects.filter(id=probation_id)
        remind_probation = ProbationReminderUserSerializer(probation, many=True).data[0]
        list_obj = []
        for item in probation_reminders:
            probation_end_date = remind_probation.get("probation_end_date")
            reminder_date = item.get("reminder_date")
            try:
                calendar = GoogleCalendar.create_probation_reminders(
                    remind_probation,
                    probation_end_date,
                    reminder_date,
                )
            except Exception:
                raise Exception("Failed to create reminder event")
            if probation_id:
                list_obj.append(
                    ProbationReminder(
                        **item,
                        probation_id=probation_id,
                        calendar_id=calendar.get("id"),
                    )
                )
            else:
                list_obj.append(
                    ProbationReminder(**item, calendar_id=calendar.get("id"))
                )

        return ProbationReminder.objects.bulk_create(list_obj)

    @classmethod
    def delete_calendar_event(cls, reminder_ids, probation_id):
        del_reminder = ProbationReminder.objects.filter(
            probation_id=probation_id
        ).exclude(id__in=reminder_ids)
        GoogleCalendar.delete_reminder_event(del_reminder)
        del_reminder.delete()

    @classmethod
    def update(cls, reminders, validated_reminders, probation_id):
        probation = Probation.objects.filter(id=probation_id)
        remind_probation = ProbationReminderUserSerializer(probation, many=True).data[0]
        probation_end_date = remind_probation.get("probation_end_date")

        reminders_objs = ProbationReminder.objects.filter(
            id__in=[reminder.get("id") for reminder in reminders]
        ).order_by("created_at")
        if reminders_objs.exists():
            for _idx, reminder in enumerate(reminders_objs):
                reminder_date = reminders[_idx].get("reminder_date")
                calendar_id = reminders[_idx].get("calendar_id")

                reminder.reminder_date = reminder_date

                try:
                    GoogleCalendar.update_reminder_event(
                        calendar_id,
                        remind_probation,
                        probation_end_date,
                        reminder_date,
                    )
                except Exception:
                    raise Exception("Failed to create reminder event")
            ProbationReminder.objects.bulk_update(
                reminders_objs,
                ["reminder_date"],
            )
        else:
            return []
        return reminders_objs

    @classmethod
    def update_reminder_status(cls, reminder_instances, change_status=0):
        for _idx, reminder in enumerate(reminder_instances):
            reminder.reminder_status = 1
        ProbationReminder.objects.bulk_update(
            reminder_instances,
            ["reminder_status"],
        )
        return reminder_instances

    @classmethod
    def check_overlap_reminder_date(cls, reminder_dates):
        reminder_set = set(reminder_dates)
        if len(reminder_set) < len(reminder_dates):
            return True
        return False

    @classmethod
    def handle_reminder_update(cls, reminders):
        reminder_dates = []
        reminder_ids = []
        update_reminders = []
        new_reminders = []
        result = dict()

        for reminder in reminders:
            reminder_dates.append(reminder.get("reminder_date"))
            reminder_ids.append(reminder.get("id"))
            if "id" in reminder:
                update_reminders.append(reminder)
            else:
                new_reminders.append(reminder)

        result.update(
            reminder_dates=reminder_dates,
            reminder_ids=reminder_ids,
            update_reminders=update_reminders,
            new_reminders=new_reminders,
        )
        return result

    @classmethod
    def create_notification_reminder(
        cls,
        assessor_name,
        reminder,
    ):
        employee_name = reminder.get("employee_name")
        probation_end_date = reminder.get("probation_end_date")
        self_evaluation_end_date = reminder.get("self_evaluation_end_date")
        is_self_evaluating = reminder.get("is_self_evaluating")
        title = "Evaluation Reminder"
        evaluation_link = "https://hrm.dev.damelagi.org/evaluations"

        main_notification = ""
        if is_self_evaluating:
            main_notification = f"*The self-evaluation of {employee_name}* will be end on *{self_evaluation_end_date}* ! \n"
        else:
            main_notification = f"*{employee_name}'s evaluation* that you are evaluating ends on *{probation_end_date}* ! \n"

        response_msg = (
            f":wave: Dear *{assessor_name}*, \n>"
            f" *Evaluation Reminder :bell:*: \n> {main_notification}"
            f"*<{evaluation_link}|Please check HRM for your evaluation !>*"
        )
        return dict(
            title=title,
            blocks=[
                SubComponentBuilder().section_mrkdwn_text_builder(
                    mrkdwn_text=response_msg
                )
            ],
        )

    @classmethod
    def get_reminder_information(cls, probation, reminder_date):
        employee_name = probation.get("employee").get("profile").get("name")
        probation_end_date = probation.get("probation_end_date")
        user_list = probation.get("reminder_user")
        self_evaluation_end_date = probation.get("self_evaluation_end_date")

        is_self_evaluating = False
        if self_evaluation_end_date:
            convert_self_end_date = datetime.strptime(
                str(self_evaluation_end_date), "%Y-%m-%d"
            ).date()
            if reminder_date <= convert_self_end_date:
                is_self_evaluating = True
                user_list = [dict(probation.get("employee").get("profile"))]
        return dict(
            employee_name=employee_name,
            probation_end_date=probation_end_date,
            user_list=user_list,
            self_evaluation_end_date=self_evaluation_end_date,
            is_self_evaluating=is_self_evaluating,
            reminder_date=reminder_date,
        )

    @classmethod
    def send_notification_slack(
        cls,
        reminder,
    ):
        for user in reminder.get("user_list"):
            channel = user.get("slack_id")
            assessor_name = user.get("name")
            print(channel)

            reminder_content = ProbationReminderService.create_notification_reminder(
                assessor_name=assessor_name,
                reminder=reminder,
            )
            try:
                slack_response_service = SlackResponseService(channel=channel)
                slack_response_service.send_message(
                    text=reminder_content.get("title"),
                    blocks=reminder_content.get("blocks"),
                )
            except Exception as e:
                return False

    @classmethod
    def update_probation_end_date(
        cls,
        channel,
        assessor_name,
        employee_name,
    ):
        reminder = ProbationReminderService.create_notification_reminder(
            assessor_name, employee_name
        )
        slack_response_service = SlackResponseService(channel=channel)
        slack_response_service.send_message(
            text=reminder.get("title"),
            blocks=reminder.get("blocks"),
        )

    @classmethod
    def update_reminder_date(cls, probation_id, probation):
        reminders = ProbationReminder.objects.select_related("probation").filter(
            probation_id=probation_id
        )
        ProbationReminder.objects.bulk_update(reminders, ["reminder_date"])
