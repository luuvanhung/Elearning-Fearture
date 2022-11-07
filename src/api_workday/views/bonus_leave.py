from api_base.views import BaseViewSet
from api_user.models import Profile
from api_workday.models import BonusLeave
from api_workday.serializers import BonusLeaveSerializer, CUBonusLeaveSerializer
from api_workday.services import BonusLeaveService
from common.constants.api_constants import HttpMethod
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class BonusLeaveViewSet(BaseViewSet):
    queryset = BonusLeave.objects.all()
    serializer_class = CUBonusLeaveSerializer
    required_alternate_scopes = {
        "create": [["bonus_leave:edit"]],
        "list": [["bonus_leave:view"], ["bonus_leave:edit"]],
        "search": [["bonus_leave:view"], ["bonus_leave:edit"]],
        "destroy": [["bonus_leave:edit"]],
        "update": [["bonus_leave:edit"]],
        "bonus_leave_user_year": [["remain_leave:view"]]
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = BonusLeaveSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        bonus_type_id = data.get('bonus_type_id')
        reason = data.get('reason')
        bonus_days = float(data.get('bonus_days', 0))
        users_pk = data.get('users_pk')

        profile_ids = Profile.objects.filter(user_id__in=users_pk).values_list('id', flat=True)

        bonus_leaves_data = [
            {'bonus_type': bonus_type_id, 'reason': reason, 'bonus_days': bonus_days, 'profile': profile_id} for
            profile_id in profile_ids
        ]

        serializer = self.get_serializer(data=bonus_leaves_data, many=True)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                BonusLeaveService.add_bonus_days_current_days_off(profile_ids, bonus_days)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=[HttpMethod.GET], detail=False)
    def search(self, request, *args, **kwargs):
        queryset = BonusLeaveService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = BonusLeaveSerializer(page, many=True).data
        return self.get_paginated_response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                destroy_leave = -instance.bonus_days
                BonusLeaveService.add_bonus_days_current_days_off([instance.profile.id], destroy_leave)
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"details": "Can't delete bonus leave"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=[HttpMethod.POST], detail=False)
    def destroy_multi_bonus(self, request, *args, **kwargs):
        bonus_leave_ids = request.data.get("bonus_leave_ids")
        if bonus_leave_ids:
            is_deleted = BonusLeaveService.destroy_multi_bonus(bonus_leave_ids)
            if is_deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"details": "Cannot deleted this bonus"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                new_bonus_days = float(request.data.get('bonus_days'))
                request.data.pop('created_at')
                if BonusLeaveService.update_current_day_off(instance.profile, instance.bonus_days, new_bonus_days):
                    serializer = self.get_serializer(instance, data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    if getattr(instance, "_prefetched_objects_cache", None):
                        # If 'prefetch_related' has been applied to a queryset, we need to
                        # forcibly invalidate the prefetch cache on the instance.
                        instance._prefetched_objects_cache = {}
                    return Response(serializer.data)
                return Response(
                    {"details": "Can't update bonus leave"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=[HttpMethod.GET], detail=False)
    def bonus_leave_user_year(self, request, *args, **kwargs):
        user_id = request.query_params.get("id")
        profile = Profile.objects.filter(user__id=user_id).first()
        return Response(BonusLeaveService.bonus_leave_user_year(profile), status=status.HTTP_200_OK)
