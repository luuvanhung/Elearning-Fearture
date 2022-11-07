from api_base.serializers import InviteSerializer
from api_base.views import BaseViewSet
from api_oauth2.permissions.api_key_permissions import HasOauth2ApiKey
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_user.models import User
from api_user.serializers import (
    ProfileSerializers,
    UserIncludeNameAndTitleSerializer,
    UserSerializer,
    VerifyUserSerializer,
)
from api_user.services import UserService
from common.constants.api_constants import HttpMethod
from common.constants.user_constants import TitleConstant
from django.db.models import F, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.string_utils import Utils


class UserViewSet(BaseViewSet):
    """
    :attr:alternate_required_scopes: dict keyed by method name with value: iterable alternate scope lists

    For each method (exp:retrieve, create, update ...), a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
       'create': [['user:create']],
       "activate": [["user:activate_user"]],
       'update': [['user:update','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']] # one of all scope array which user scope had => permitted
    }
    Can define scope if you need, check in scopes.json file if scope doesn't exist please add it follow template
    """

    queryset = User.objects.select_related("profile")
    serializer_class = UserSerializer
    permission_classes = [TokenHasActionScope | HasOauth2ApiKey]
    required_alternate_scopes = {
        "create": [
            ["user:access_personal"],
            ["user:edit_public_user_information_list"],
        ],
        "retrieve": [
            ["user:access_personal"],
            ["user:view_public_user_information_list"],
        ],
        "update": [
            ["user:access_personal"],
            ["user:edit_public_user_information_list"],
        ],
        "destroy": [
            ["user:access_personal"],
            ["user:edit_public_user_information_list"],
        ],
        "deactivate": [
            ["user:access_personal"],
            ["user:edit_public_user_information_list"],
        ],
        "list": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "search": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "get_non_paginate": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "get_latest_five": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "search_non_paginate": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "activate": [["user:activate_user"]],
        "change_password": [["user:access_personal"]],
        "get_project_managers": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "get_all_title": [["user:view_public_user_information_list"], ["user:access_personal"]],
        "get_users_include_name_and_title": [
            ["user:view_public_user_information_list"],
            ["user:access_personal"]
        ],
        "import_users": [["user:edit_public_user_information_list"]],
    }

    def create(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        if invite_serializer.is_valid(raise_exception=True):
            email = request.data.get("email")
            name = request.data.get("name")
            base_link = request.build_absolute_uri("/verify")
            res = UserService.invite(email, name, base_link)
            return Response(res)

    @action(detail=False, methods=[HttpMethod.POST], url_path="import-users")
    def import_users(self, request, *args, **kwargs):
        data = request.data
        if not data:
            return Response({"error": "Empty data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            base_link = request.build_absolute_uri("/verify")
            valid_user, invalid_user = UserService.import_users(data, base_link)
            res = {"valid_user": valid_user, "invalid_user": invalid_user}
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        query_name = self.request.query_params.get("name", None)
        if query_name:
            queryset = self.queryset.filter(profile__name__istartswith=query_name).order_by("profile")
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by("profile")
            active = self.request.query_params.get("active")
            if active:
                queryset = queryset.filter(Q(active=1 and Utils.convert_to_int(active)))
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_non_paginate(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(active=True)
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all_existed_accounts(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_latest_five(self, request, *args, **kwargs):
        queryset = (
            self.filter_queryset(self.get_queryset())
            .filter(active=True)
            .order_by("-timestamp")[:5]
        )
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all_exclude_user(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("id", None)
        queryset = (
            self.filter_queryset(self.get_queryset())
            .filter(active=True)
            .exclude(id=user_id)
        )
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=[HttpMethod.GET], detail=False)
    def search(self, request, *args, **kwargs):
        queryset = UserService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def search_non_paginate(self, request, *args, **kwargs):
        queryset = UserService.get_filter_query(request)
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    @action(methods=[HttpMethod.PUT], detail=True)
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.activate_user(user)
        return Response({"Success": True})

    @action(methods=[HttpMethod.PUT], detail=True)
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.deactivate_user(user)
        return Response({"Success": True}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.PUT], detail=True)
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        error_message = UserService.update_password(request.data, user)
        if error_message:
            return Response(
                {"Success": False, "msg": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_update(user)
        return Response({"Success": True})

    @action(methods=[HttpMethod.GET], detail=False)
    def get_project_managers(self, request, *args, **kwargs):
        queryset = self.queryset.filter(title=TitleConstant.PROJECT_MANAGER)
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all_title(self, request, *args, **kwargs):
        queryset = User.objects.values("title").distinct()
        return Response(dict(data=queryset))

    @action(methods=[HttpMethod.GET], detail=False)
    def get_users_include_name_and_title(self, request, *args, **kwargs):
        query_set = User.objects.all()
        serializer = UserIncludeNameAndTitleSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_line_manager(self, request, *args, **kwargs):
        try:
            user_id = self.request.query_params.get("id", None)
            query_set = User.objects.select_related("profile").filter(id=user_id)
            profile_obj = query_set[0].profile.line_manager
            return Response(
                ProfileSerializers(profile_obj).data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_users_include_line_manager(self, request, *args, **kwargs):
        try:
            user_id = self.request.query_params.get("user_id", None)
            queryset = (
                User.objects.select_related("profile", "title", "team")
                .filter(id=user_id)
                .values(
                    "id",
                    "title",
                    title_name=F("title__title"),
                    user_name=F("profile__name"),
                    line_manage_name=F("profile__line_manager__name"),
                    line_manager_user_id=F("profile__line_manager__user_id"),
                    join_date=F("profile__join_date"),
                )
            )
            return Response(queryset, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.GET], detail=False)
    def get_users_filter_title(self, request, *args, **kwargs):
        try:
            title = self.request.query_params.get("title", None)
            query_set = User.objects.filter(title__title=title)
            page = self.paginate_queryset(query_set)
            data = self.get_serializer(page, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.POST], detail=False, permission_classes=[])
    def verify(self, request, *args, **kwargs):
        serializer = VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.set_password(
            serializer.data.get("email"), serializer.data.get("password")
        )
        return Response("Success", status=status.HTTP_200_OK)
