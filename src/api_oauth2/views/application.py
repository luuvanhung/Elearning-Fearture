import uuid

from api_base.views import BaseViewSet
from api_oauth2.models import Application
from api_oauth2.serializers import (
    ApplicationCreateSerializer,
    ApplicationRetrieveSerializer,
    ApplicationSerializer,
    ApplicationUpdateSerializer,
    SimpleApplicationSerializer,
)
from api_oauth2.services.application import ApplicationService
from common.constants.api_constants import HttpMethod
from common.constants.api_oauth2.scope import Scope
from core.settings.base import DEFAULT_SCOPES, SCOPES
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class ApplicationViewSet(BaseViewSet):
    serializer_class = ApplicationSerializer
    serializer_map = {
        "list": SimpleApplicationSerializer,
        "create": ApplicationCreateSerializer,
        "update": ApplicationUpdateSerializer,
    }
    required_alternate_scopes = {
        "destroy": [["application:update"]],
        "update": [["application:update"]],
        "create": [["application:create"]],
        "retrieve": [["application:retrieve"]],
        "list": [["application:list"]],
    }
    lookup_field = "client_id"

    def get_queryset(self):
        queryset = ApplicationService.get_list(self.request)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        post_user_id = data.get("user_id")
        if post_user_id:
            post_user_id = uuid.UUID(post_user_id)
            if request.user.id != post_user_id:
                raise ValidationError(
                    {"user_id": f"Can't create applications with id: {post_user_id}"}
                )
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return_obj = serializer.save()
            return Response(
                self.serializer_class(return_obj).data,
                status=status.HTTP_201_CREATED,
            )

    def update(self, request, *args, **kwargs):
        data: dict = request.data.copy()
        obj: Application = self.get_object()
        serializer = self.get_serializer(obj, data=data)
        if serializer.is_valid(raise_exception=True):
            return_obj = serializer.save()
            return Response(
                self.serializer_class(return_obj).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"user": "You dont have permission for update application"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=[HttpMethod.GET], detail=True)
    def retrieve_application_scopes(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ApplicationRetrieveSerializer(instance)
        return Response(serializer.data)

    @action(methods=[HttpMethod.GET], detail=False)
    def retrieve_all_scopes(self, request, *args, **kwargs):
        scope_dict = SCOPES
        default_scope_dict = DEFAULT_SCOPES
        group = {}
        for key in scope_dict.keys():
            if key != "*":
                resource = Scope.GROUP_SCOPE.get(key.split(":")[0].strip())
                if resource not in group:
                    group[resource] = []
                    group.get(resource).append(
                        {"scope": key, "label": scope_dict.get(key), "disabled": key in default_scope_dict}
                    )
                else:
                    group.get(resource).append(
                        {"scope": key, "label": scope_dict.get(key), "disabled": key in default_scope_dict}
                    )
        result = []
        for key in group.keys():
            result.append({"scope": key, "label": key, "children": group[key]})
        return Response({"scope": result})
