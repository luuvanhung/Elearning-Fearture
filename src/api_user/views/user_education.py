from api_base.views import BaseViewSet
from api_user.models.user import User
from api_user.models.user_education import UserEducation
from api_user.permissions import IsOwnerOrHasScope
from api_user.serializers.related_profile import UserEducationSerializer
from common.constants.api_constants import HttpMethod
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.string_utils import Utils


class UserEducationViewSet(BaseViewSet):
    serializer_class = UserEducationSerializer
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
        self.check_object_permissions(self.request, user)
        education = UserEducation.objects.filter(user=user)
        education_serializer = self.get_serializer(education, many=True)
        return Response(education_serializer.data)

    @action(methods=[HttpMethod.POST], detail=True)
    def add(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        self.check_object_permissions(self.request, user)
        education_serializer = self.get_serializer(data=request.data)
        education_serializer.is_valid(raise_exception=True)
        education_serializer.save(user=user)
        return Response(education_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        education_id = data.get("id")
        if not (education_id and Utils.is_valid_uuid(education_id)):
            data = {"detail": "invalid education id"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        education = UserEducation.objects.filter(pk=education_id).first()
        self.check_object_permissions(self.request, education)
        education_serializer = self.get_serializer(
            education, data=request.data, partial=True
        )
        education_serializer.is_valid(raise_exception=True)
        self.perform_update(education_serializer)
        return Response(education_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = UserEducation.objects.filter(user=kwargs.get("pk"))
        self.check_object_permissions(self.request, instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
