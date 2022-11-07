from api_base.services import BaseService
from api_workday.models import RequestOff
from api_workday.models.leave_type import LeaveType
from api_workday.serializers.leave_type import LeaveTypeSerializer
from django.db import transaction
from django.db.models import Max


class LeaveTypeService(BaseService):
    @classmethod
    def get_all_leave_type(cls):
        leave_type = LeaveType.objects.filter(is_active=True)
        serializer = LeaveTypeSerializer(leave_type, many=True)
        return serializer.data

    @classmethod
    def get_leave_type_by_id(cls, leave_type_id: str):
        return LeaveType.objects.filter(pk=leave_type_id, is_active=True).first()

    @classmethod
    def get_leave_type_by_name(cls, leave_type_name: str):
        return LeaveType.objects.filter(name=leave_type_name, is_active=True).first()

    @classmethod
    def get_longest_duration_and_is_company_pay_leave_type(cls):
        leave_type = (
            LeaveType.objects.filter(leave_type_group__is_company_pay=True)
            .annotate(biggest_quantity_days=Max("days"))
            .order_by("-biggest_quantity_days")
        )
        serializer = LeaveTypeSerializer(leave_type.first(), many=False)
        return serializer.data

    @classmethod
    def destroy(cls, leave_type):
        try:
            with transaction.atomic():
                from api_workday.services import ActionRequestService
                requests_off = RequestOff.objects.filter(leave_type=leave_type)
                if requests_off.exists():
                    request_offs_return_day_off = filter(lambda
                                                             request_off: request_off.leave_type.leave_type_group.is_company_pay and request_off.leave_type.is_count,
                                                         requests_off)
                    ActionRequestService.handle_return_day_off_for_request(request_offs_return_day_off)
                    requests_off.delete()
                leave_type.delete()
            return True
        except Exception as e:
            return False
