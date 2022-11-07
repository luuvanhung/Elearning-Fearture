from datetime import date

from api_base.services.sendprobation import SendProbation
from api_probation.models import Probation, ProbationReminder
from api_probation.serializers.probation import ProbationReminderUserSerializer
from api_probation.services.probation_reminder import ProbationReminderService


def get_probation_reminder_today():
    print("Start send probation remind")
    today = date.today()
    reminder_data = ProbationReminder.objects.filter(
        reminder_date=today, reminder_status=0
    ).in_bulk(field_name="id")
    reminder_ids = list(reminder_data.keys())
    reminder_instances = list(reminder_data.values())
    queryset = Probation.objects.filter(reminders__id__in=reminder_ids)
    serializer = ProbationReminderUserSerializer(queryset, many=True)
    for probation in serializer.data:
        SendProbation.start(
            probation=probation,
            reminder_date=today,
        )
    ProbationReminderService.update_reminder_status(reminder_instances, change_status=1)
    print("Finish send probation remind")
