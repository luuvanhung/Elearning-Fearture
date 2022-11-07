import threading

from api_probation.services.probation_reminder import ProbationReminderService


class ProbationThread(threading.Thread):
    def __init__(
        self,
        probation=None,
        reminder_date=None,
    ):
        self.probation = probation
        self.reminder_date = reminder_date
        threading.Thread.__init__(self)

    def run(self):
        try:
            reminder = ProbationReminderService.get_reminder_information(
                probation=self.probation, reminder_date=self.reminder_date
            )
            ProbationReminderService.send_notification_slack(reminder)

        except Exception as e:
            print(str(e))


class SendProbation:
    @staticmethod
    def start(
        probation,
        reminder_date,
    ):
        ProbationThread(
            probation=probation,
            reminder_date=reminder_date,
        ).start()
