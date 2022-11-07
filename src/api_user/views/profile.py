from api_base.views import BaseViewSet
from api_lunch.services import LunchServices
from api_oauth2.permissions import TokenHasActionScope
from api_user.models.profile import Profile
from api_user.serializers import ProfileAvatar, ProfileLunch, ProfileSerializers
from api_user.services.profile import ProfileService
from api_user_lunch.services import UserLunchServices
from api_workday.services import RemainLeaveService
from common.constants.api_constants import HttpMethod
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ProfileViewSet(BaseViewSet):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializers
    pagination_class = None
    permission_classes = [TokenHasActionScope]

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
        "destroy": [["user:edit_public_user_information_list"]],
        "list": [["user:view_public_user_information_list"]],
        "get_auto_booking_lunch_profiles": [["user_lunch:update_list_auto_booking"]],
        "update_auto_booking": [["user:access_personal"]],
        "update_list_auto_booking": [["user_lunch:update_list_auto_booking"]],
        "get_profile_lunch": [["user:view_public_user_information_list"]],
        "update_veggie_user": [["user:access_personal"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.email = instance.user.email
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.auth.scope.find(
            "user:edit_public_user_information_list"
        ) != -1 or str(request.user.profile.id) == kwargs.get("pk"):
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            old_join_date = instance.join_date
            with transaction.atomic():
                self.perform_update(serializer)
                RemainLeaveService.update_remain_leave_by_profile(instance, old_join_date)
            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(methods=[HttpMethod.PATCH], detail=True)
    def change_avatar(self, request, *args, **kwargs):
        if request.auth.scope.find(
            "user:edit_public_user_information_list"
        ) != -1 or str(request.user.profile.id) == kwargs.get("pk"):
            profile = self.get_object()
            serializer = ProfileAvatar(
                profile, data=request.data, partial=True
            )  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"detail": "Data is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"detail": "you dont have permission"}, status=status.HTTP_403_FORBIDDEN
            )

    @action(methods=[HttpMethod.GET], detail=False)
    def get_auto_booking_lunch_profiles(self, request, *args, **kwargs):
        pfs_lunch_booking = Profile.objects.filter(auto_booking_lunch=True, user__active=True)
        pfs_lunch_not_booking = Profile.objects.filter(auto_booking_lunch=False, user__active=True)
        data = {
            "pfs_lunch_booking": self.get_serializer(
                pfs_lunch_booking, many=True, context={"request": request}
            ).data,
            "pfs_lunch_not_booking": self.get_serializer(
                pfs_lunch_not_booking, many=True, context={"request": request}
            ).data,
        }
        return Response(data)

    @action(methods=[HttpMethod.PUT], detail=True)
    def update_lunch(self, request, *args, **kwargs):
        # TODO Create a service/update validate for ProfileLunch for this
        data = request.data.copy()
        # TODO Check UI again for all this, after update, remove below codes
        # FIXME veggie param need to be 0/1 instead

        data.update(
            veggie=True if data.get("veggie") == "true" else False,
        )
        # TODO Remove to here

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ProfileLunch(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        LunchServices.update_lunch(instance)

        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.GET], detail=True)
    def get_profile_lunch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileLunch(instance)
        return Response(serializer.data)

    @action(methods=[HttpMethod.POST], detail=True)
    def set_line_manager(self, request, *args, **kwargs):
        data = request.data.copy()
        personal_email = data.get("personal_email")
        manager_profile = self.queryset.filter(personal_email=personal_email).first()
        if not manager_profile:
            data = {"detail": "Profile of this user not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        current_user = get_object_or_404(Profile, pk=kwargs.get("pk"))
        if current_user.id == manager_profile.id:
            data = {"detail": "Can not assign manager by itself"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if current_user == manager_profile.line_manager:
            data = {"detail": "You are manager of this user"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        current_user.line_manager = manager_profile
        current_user.save()
        data = {"manager_id": manager_profile.user.id}
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=True)
    def set_level_approved(self, request, *args, **kwargs):
        data = request.data.copy()
        level = data.get("level")
        current_profile = self.queryset.filter(pk=kwargs.get("pk")).first()
        if not current_profile:
            data = {"detail": "User not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        current_profile.maximum_level_approved = level
        current_profile.save()
        data = {"level": current_profile.maximum_level_approved}
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.DELETE], detail=True)
    def remove_line_manager(self, request, *args, **kwargs):
        current_user = get_object_or_404(Profile, pk=kwargs.get("pk"))
        current_user.line_manager = None
        current_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.PUT], detail=True)
    def update_auto_booking(self, request, *args, **kwargs):
        current_user = get_object_or_404(Profile, pk=kwargs.get("pk"))
        current_user.auto_booking_lunch = request.data.get("auto_booking_lunch")
        current_user.save()
        data = {
            "auto_booking_lunch": current_user.auto_booking_lunch,
            "veggie": current_user.veggie,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.PUT], detail=False)
    def update_list_auto_booking(self, request, *args, **kwargs):
        profiles = request.data.get("profiles")
        auto_booking_lunch = request.data.get("auto_booking_lunch")
        update_profiles = ProfileService.update_list_auto_booking(
            profiles, auto_booking_lunch
        )
        if auto_booking_lunch:
            UserLunchServices.create_many_for_employees(data_user_lunches=profiles)
        return Response(update_profiles, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HttpMethod.PUT], detail=True)
    def update_veggie_user(self, request, *args, **kwargs):
        current_user = get_object_or_404(Profile, pk=kwargs.get("pk"))
        current_user.veggie = request.data.get("veggie")
        current_user.save()
        data = {"veggie": current_user.veggie}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
