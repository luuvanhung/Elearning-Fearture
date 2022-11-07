from api_slackbot.models import TempLeaveRequest
from api_slackbot.serializers.temp_leave_request import TempLeaveRequestSerializer
from common.constants.workday_constants.leave_type import Leave
from django.db import transaction


class TempLeaveRequestService:
    @classmethod
    def create_temp_leave_request(
        cls,
        profile_id,
        request_date,
        leave_type_id=None,
        lunch_status=False,
        full_day_leave_lunch_flag=False,
        reason=Leave.DEFAULT_LEAVE_REASON,
    ):
        request_transferred_model_object = {
            "leave_type_id": leave_type_id,
            "profile_id": profile_id,
            "from_date": request_date.get("from_date"),
            "from_time": request_date.get("from_time"),
            "to_date": request_date.get("to_date"),
            "to_time": request_date.get("to_time"),
            "lunch_status": lunch_status,
            "full_day_leave_lunch_flag": full_day_leave_lunch_flag,
            "reason": reason,
        }

        temp_leave_request_serializer = TempLeaveRequestSerializer(
            data=request_transferred_model_object
        )

        with transaction.atomic():
            if temp_leave_request_serializer.is_valid():
                return temp_leave_request_serializer.save(
                    leave_type_id=request_transferred_model_object.get("leave_type_id"),
                    profile_id=request_transferred_model_object.get("profile_id"),
                    from_date=request_transferred_model_object.get("from_date"),
                    from_time=request_transferred_model_object.get("from_time"),
                    to_date=request_transferred_model_object.get("to_date"),
                    to_time=request_transferred_model_object.get("to_time"),
                    reason=request_transferred_model_object.get("reason"),
                ).id

    @classmethod
    def get_temp_leave_request_by_id(cls, temp_leave_request_id):
        return TempLeaveRequest.objects.filter(pk=temp_leave_request_id).first()

    @classmethod
    def get_temp_leave_request_by_profile_id_and_from_datetime(
        cls, profile_id, from_date, from_time
    ):
        return TempLeaveRequest.objects.filter(
            profile_id=profile_id, from_date=from_date, from_time=from_time
        ).first()

    @classmethod
    def update_leave_type_by_id(cls, temp_leave_request_id, leave_type_id):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            leave_type_id=leave_type_id
        )

    @classmethod
    def update_from_date_by_id(cls, temp_leave_request_id, selected_date):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            from_date=selected_date
        )

    @classmethod
    def update_from_time_by_id(cls, temp_leave_request_id, selected_time):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            from_time=selected_time
        )

    @classmethod
    def update_to_date_by_id(cls, temp_leave_request_id, selected_date):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            to_date=selected_date
        )

    @classmethod
    def update_to_time_by_id(cls, temp_leave_request_id, selected_time):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            to_time=selected_time
        )

    @classmethod
    def update_lunch_status_by_id(cls, temp_leave_request_id, value: bool):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            lunch_status=value
        )

    @classmethod
    def update_full_leave_lunch_flag_by_id(cls, temp_leave_request_id, value: bool):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(
            full_day_leave_lunch_flag=value
        )

    @classmethod
    def update_reason_by_id(cls, temp_leave_request_id, reason: str):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).update(reason=reason)

    @classmethod
    def delete_temp_leave_request_if_exist_by_id(cls, temp_leave_request_id):
        TempLeaveRequest.objects.filter(pk=temp_leave_request_id).delete()

    @classmethod
    def delete_temp_leave_request_if_exist_by_profile_id(cls, profile_id):
        TempLeaveRequest.objects.filter(profile_id=profile_id).delete()

    @classmethod
    def delete_temp_leave_request_if_exist_by_profile_id_and_from_datetime(
        cls, profile_id, from_date, from_time
    ):
        TempLeaveRequest.objects.filter(
            profile_id=profile_id, from_date=from_date, from_time=from_time
        ).delete()

    @classmethod
    def delete_all_temp_leave_request(cls):
        TempLeaveRequest.objects.all().delete()
