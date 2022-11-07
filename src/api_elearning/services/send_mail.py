from django.db.models import Q
import datetime
from api_base.services.sendmail import SendMail
from api_elearning.models import Assignment
from api_elearning.constants.status import AssignmentContentStatus
from django.conf import settings
from django.template.loader import render_to_string


class SendEmailNotification:
    url_logo = "http://{}:{}/static/paradoxlogo.png".format(
        settings.API_HOST, settings.API_PORT
    )

    @classmethod
    def send_new_assignment_notification(cls, assignment):
        link = settings.URL_WEB_INTERNAL
        if link[-1] == "/":
            link = link[:-1]
        assignments_list = Assignment.objects.filter(user=assignment.user)
        content = render_to_string(
            "../templates/new_assignment_notification.html",
            {
                "logo": cls.url_logo,
                "name": assignment.full_name,
                "title": assignment.course_name,
                "assignments_list": assignments_list,
                "link": link,
                "due_date": assignment.due_date,
                "id": assignment.id
            },
        )
        user_emails = []
        if assignment.user.email:
            user_emails.append(assignment.user.email)
        SendMail.start(user_emails, "You've been enrolled in training", content)

    @classmethod
    def send_assignments_reminder(cls, assignments):
        users = []
        link = settings.URL_WEB_INTERNAL
        if link[-1] == "/":
            link = link[:-1]
        for assignment in assignments:
            if assignment.user not in users:
                users.append(assignment.user)

        for user in users:
            user_assignments = [assignment for assignment in assignments if assignment.user == user]
            for user_assignment in user_assignments:
                if user_assignment.due_date:
                    user_assignment.date_left = (
                            user_assignment.due_date - datetime.datetime.now()
                    ).days
                else:
                    user_assignment.date_left = None

            content = render_to_string(
                "../templates/assignment_reminder.html",
                {
                    "logo": cls.url_logo,
                    "name": user.profile.name,
                    "assignments_list": user_assignments,
                    "link": link,
                },
            )
            if user.email:
                SendMail.start([user.email], "Please complete your assigned training!", content)
