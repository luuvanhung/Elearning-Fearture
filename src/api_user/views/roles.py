from api_base.views import BaseViewSet
from api_user.models.roles import Role
from api_user.serializers.roles import RoleSerializer
from common.constants.message import ResponseMessages
from rest_framework import status
from rest_framework.response import Response


class RoleViewSet(BaseViewSet):
    """
    :attr:alternate_required_scopes: dict keyed by method name with value: iterable alternate scope lists

    For each method (exp:retrieve, create, update ...), a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
        'create': [['role:create']],
        'update': [['role:update','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']] # one of all scope array which user scope had => permitted
    }
    Can define scope if you need, check in scopes.json file if scope doesn't exist please add it follow template
    """

    queryset = Role.objects.exclude(name__exact="Super Administrator")
    serializer_class = RoleSerializer
    required_alternate_scopes = {
        "create": [["role:edit"]],
        "retrieve": [["role:view"]],
        "update": [["role:edit"]],
        "destroy": [["role:edit"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data.update({"last_modified_by": request.user.profile.name})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": ResponseMessages.get_response_message(ResponseMessages.CREATED, params=["Role"]), "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.initial_data.update({"last_modified_by": request.user.profile.name})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {"message": ResponseMessages.get_response_message(ResponseMessages.UPDATED, params=["Role"]), "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": ResponseMessages.get_response_message(ResponseMessages.DELETED, params=["Role"])}, status=status.HTTP_204_NO_CONTENT)
