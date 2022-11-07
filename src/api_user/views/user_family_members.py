from api_base.views import BaseViewSet
from api_user.models.user import User
from api_user.models.user_family_members import UserFamilyMembers
from api_user.permissions import IsOwnerOrHasScope
from api_user.serializers.related_profile import UserFamilyMembersSerializer
from common.constants.api_constants import HttpMethod
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.string_utils import Utils


class UserFamilyMembersViewSet(BaseViewSet):
    serializer_class = UserFamilyMembersSerializer
    permission_classes = [IsOwnerOrHasScope]

    required_alternate_scopes = {
        "create": [["user:edit_private_user_information_list"]],
        "retrieve": [["user:view_private_user_information_list"]],
        "update": [["user:edit_private_user_information_list"]],
        "destroy": [["user:edit_private_user_information_list"]],
        "add": [["user:edit_private_user_information_list"]],
        "list": [["user:view_private_user_information_list"]],
    }

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        family_members = UserFamilyMembers.objects.filter(user=user)
        family_members_serializer = self.get_serializer(family_members, many=True)
        return Response(family_members_serializer.data)

    @action(methods=[HttpMethod.POST], detail=True)
    def add(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        family_members_serializer = self.get_serializer(data=request.data)
        family_members_serializer.is_valid(raise_exception=True)
        family_members_serializer.save(user=user)
        return Response(family_members_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        family_member_id = data.get("id")
        if not (family_member_id and Utils.is_valid_uuid(family_member_id)):
            data = {"detail": "invalid family member id"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        family_members = UserFamilyMembers.objects.filter(pk=family_member_id).first()
        family_members_serializer = self.get_serializer(
            family_members, data=request.data, partial=True
        )
        family_members_serializer.is_valid(raise_exception=True)
        self.perform_update(family_members_serializer)
        return Response(family_members_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = UserFamilyMembers.objects.get(pk=kwargs.get("pk"))
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
