from api_base.views import BaseViewSet
from api_user.models.user import User
from api_user.models.user_banks import UserBanks
from api_user.permissions import IsOwnerOrHasScope
from api_user.serializers.related_profile import UserBanksSerializer
from common.constants.api_constants import HttpMethod
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserBankViewSet(BaseViewSet):
    serializer_class = UserBanksSerializer
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
        bank = UserBanks.objects.filter(user=user).first()
        if not bank:
            data = {"detail": "User bank information not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        bank_serializer = self.get_serializer(bank)
        return Response(bank_serializer.data)

    @action(methods=[HttpMethod.POST], detail=True)
    def add(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        self.check_object_permissions(self.request, user)
        bank_serializer = self.get_serializer(data=request.data)
        bank_serializer.is_valid(raise_exception=True)
        try:
            bank_serializer.save(user=user)
        except IntegrityError:
            data = {"detail": "User bank information already exist"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(bank_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        bank = UserBanks.objects.filter(user=user).first()
        if not bank:
            data = {"detail": "bank information not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        bank_serializer = self.get_serializer(bank, data=request.data, partial=True)
        self.check_object_permissions(self.request, bank)
        bank_serializer.is_valid(raise_exception=True)
        self.perform_update(bank_serializer)
        return Response(bank_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        bank = UserBanks.objects.filter(user=user).first()
        if not bank:
            data = {"detail": "User bank information not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, bank)
        UserBanks.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
