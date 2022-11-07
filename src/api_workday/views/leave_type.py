from api_base.views import BaseViewSet
from api_workday.models.leave_type import LeaveType
from api_workday.serializers.leave_type import LeaveTypeSerializer
from api_workday.services.leave_type import LeaveTypeService
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class LeaveTypeViewSet(BaseViewSet):
    serializer_class = LeaveTypeSerializer
    queryset = LeaveType.objects
    pagination_class = None
    required_alternate_scopes = {
        "create": [["type_off:edit"]],
        "retrieve": [["type_off:view"]],
        "update": [["type_off:edit"]],
        "partial_update": [["type_off:edit"]],
        "destroy": [["type_off:edit"]],
        "list": [["type_off:view"]],
        "list_type_true": [["type_off:view"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def list_type_true(self, request, *args, **kwargs):
        data = LeaveTypeService.get_all_leave_type()
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.save() is not None:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Create Type Leaves Failed"}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, *args, **kwargs):
        leave_type = LeaveType.objects.get(pk=kwargs["pk"])
        serializer = LeaveTypeSerializer(
            leave_type, data={"is_active": leave_type.is_active is False}, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        leave_type = self.get_object()
        is_deleted = LeaveTypeService.destroy(leave_type)
        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "Cannot deleted this record"}, status=status.HTTP_400_BAD_REQUEST)
