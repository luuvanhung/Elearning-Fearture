from api_base.views import BaseViewSet
from api_session.models import Session
from api_session.serializers import SessionSerializer
from common import Utils
from common.constants.api_constants import HttpMethod
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class SessionViewSet(BaseViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "create_multiple": [["office:edit"]],
        "delete_by_dow": [["office:edit"]],
        "list": [["office:view"]],
        "get_by_profile": [["office:view"]],
        "get_by_office_id": [["office:view"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_by_office_id(self, request, *args, **kwargs):
        office_id = Utils.cast_to_int(
            self.request.query_params.get("office_id", None), None
        )
        if office_id is None:
            return Response(
                {"detail": "office id param not found in url"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            self.get_queryset().filter(office_id=office_id), many=True
        )
        return Response(serializer.data)

    @action(methods=[HttpMethod.DELETE], detail=False)
    def delete_by_dow(self, request, *args, **kwargs):
        dow_param = Utils.cast_to_int(self.request.query_params.get("dow", None), None)
        office_id = Utils.cast_to_int(
            self.request.query_params.get("office_id", None), None
        )
        if dow_param is None:
            return Response(
                {"detail": "dow param not found in url"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if office_id is None:
            return Response(
                {"detail": "office id param not found in url"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Session.objects.filter(dow=dow_param, office_id=office_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_by_profile(self, request, *args, **kwargs):
        profile = request.user.profile
        sessions = Session.objects.filter(office=profile.office)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    @action(methods=[HttpMethod.POST], detail=False)
    def create_multiple(self, request, *args, **kwargs):
        data = request.data
        dow = data.get("dow", None)
        office_id = data.get("office", None)
        sessions = data.get("sessions", [])

        if dow is None:
            return Response(
                {"detail": "dow field is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        if office_id is None:
            return Response(
                {"detail": "office_id field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not sessions:
            return Response(
                {"detail": "sessions field is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for session in sessions:
            session["dow"] = dow
            session["office"] = office_id

        with transaction.atomic():
            serializer = self.get_serializer(data=sessions, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
