from api_probation.models import ProbationReminder
from api_probation.services.probation_reminder import ProbationReminderService
from rest_framework import serializers


class ListProbationReminderSerializer(serializers.ListSerializer):
    def create(self, probation_reminders):
        probation_id = self.context.get("probation_id") or None
        return ProbationReminderService.create(probation_reminders, probation_id)

    def update(self, reminders, new_reminders):
        probation_id = self.context.get("probation_id") or None
        return ProbationReminderService.update(reminders, new_reminders, probation_id)

    class Meta:
        model = ProbationReminder
        fields = "__all__"


class ProbationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationReminder
        list_serializer_class = ListProbationReminderSerializer
        exclude = ["probation"]
