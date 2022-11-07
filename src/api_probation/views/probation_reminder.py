from api_base.views import BaseViewSet
from api_probation.models import ProbationReminder
from api_probation.serializers.probation_reminder import ProbationReminderSerializer
from api_probation.services.probation_reminder import ProbationReminderService
from common.constants.api_constants import HttpMethod
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ProbationReminderViewSet(BaseViewSet):
    queryset = ProbationReminder.objects
    serializer_class = ProbationReminderSerializer
    required_alternate_scopes = {}

    @action(methods=[HttpMethod.GET], detail=False)
    def get_reminder_detail(self, request, *args, **kwargs):
        try:
            probation_id = self.request.query_params.get("probation_id", None)
            reminder = self.queryset.filter(
                probation_id=probation_id, reminder_status=0
            ).order_by("created_at")
            serializer = ProbationReminderSerializer(reminder, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=False)
    def create_reminders(self, request, *args, **kwargs):
        probation_id = self.request.query_params.get("probation_id", None)
        reminders = request.data.copy()
        reminder_dates = [reminder["reminder_date"] for reminder in reminders]

        try:
            with transaction.atomic():
                if ProbationReminderService.check_overlap_reminder_date(reminder_dates):
                    return Response(
                        {"error": "There already exist reminder date"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    reminder_serializer = self.serializer_class(
                        data=reminders,
                        many=True,
                        context={"probation_id": probation_id},
                    )
                    if reminder_serializer.is_valid(raise_exception=True):
                        self.perform_create(reminder_serializer)
                    return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "New reminders created error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=[HttpMethod.PUT], detail=False)
    def update_reminders(self, request, *args, **kwargs):
        probation_id = self.request.query_params.get("probation_id", None)
        request_data = request.data.copy()
        data = ProbationReminderService.handle_reminder_update(request_data)
        try:
            with transaction.atomic():
                if ProbationReminderService.check_overlap_reminder_date(
                    data.get("reminder_dates")
                ):
                    return Response(
                        {"error": "There already exist reminder date"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    reminder_ids = data.get("reminder_ids")
                    ProbationReminderService.delete_calendar_event(
                        reminder_ids, probation_id
                    )
                    update_reminder_serializer = self.serializer_class(
                        data.get("update_reminders"),
                        data=data.get("update_reminders"),
                        many=True,
                        context={"probation_id": probation_id},
                        partial=True,
                    )
                    if update_reminder_serializer.is_valid(raise_exception=True):
                        self.perform_update(update_reminder_serializer)
                    create_reminder_serializer = self.serializer_class(
                        data=data.get("new_reminders"),
                        many=True,
                        context={"probation_id": probation_id},
                    )
                    if create_reminder_serializer.is_valid(raise_exception=True):
                        self.perform_create(create_reminder_serializer)
                    return Response({"msg": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "New reminders updated error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
