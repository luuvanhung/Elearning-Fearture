from api_base.views.base import BaseViewSet
from api_wfh.models.wfh_date import WfhDate
from api_wfh.serializers.wfh_date import WfhDateSerializer
from rest_framework import status
from rest_framework.response import Response


class WfhDateViewSet(BaseViewSet):
    queryset = WfhDate.objects.all()
    serializer_class = WfhDateSerializer

    def create(self, request, *args, **kwargs):
        serializer = WfhDateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
