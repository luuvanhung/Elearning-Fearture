from api_slackbot.models import TempLeaveRequest


def delete_temp_leave_request():
    TempLeaveRequest.objects.all().delete()
