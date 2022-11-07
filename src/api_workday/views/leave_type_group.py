from api_base.views import BaseViewSet
from rest_framework import status
from rest_framework.response import Response

from ..models.leave_type_group import LeaveTypeGroup
from ..serializers.leave_type_group import LeaveTypeGroupSerializer


class LeaveTypeGroupViewSet(BaseViewSet):
    queryset = LeaveTypeGroup.objects
    serializer_class = LeaveTypeGroupSerializer
    pagination_class = None
    required_alternate_scopes = {
        "create": [["type_pay:edit"]],
        "retrieve": [["type_pay:view"]],
        "update": [["type_pay:edit"]],
        "destroy": [["type_pay:edit"]],
        "list": [["type_pay:view"]],
    }

    def create(self, request, *args, **kwargs):
        serializer = LeaveTypeGroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.save() is not None:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Create Type Pay Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
