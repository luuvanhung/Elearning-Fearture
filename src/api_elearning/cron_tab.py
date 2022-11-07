from django.db.models import Q

from api_elearning.models import Assignment
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.services.send_mail import SendEmailNotification
from api_elearning.services.send_notification_slack import SendSlackNotification


def send_assignments_reminder():
    open_assignments = Assignment.objects.filter(Q(status=AssignmentContentStatus.OPEN.value)).order_by('user')
    if open_assignments:
        SendSlackNotification.send_assignments_reminder(open_assignments)
        SendEmailNotification.send_assignments_reminder(open_assignments)
