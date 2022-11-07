import datetime

from api_oauth2.permissions.oauth2_permissions import CustomTokenMatchesOASRequirements
from common.constants.api_constants import HttpMethod
from common.constants.lunch_constants import Lunch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import UserLunch
from .serializers import CreateUserLunchSerializer, UserLunchSerializer
from .services import UserLunchServices


class GetUserLunches(ListAPIView):
    queryset = UserLunch.objects.all()
    filterset_fields = ["date"]
    serializer_class = UserLunchSerializer
    ordering_fields = ["date"]
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user:view_public_user_information_list"], ["user:access_personal"]],
    }

    def get_queryset(self):
        return self.queryset


class GetAllUserLunches(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user_lunch:get_all"]],
    }

    def get(self, request):
        queryset = UserLunch.objects.all()
        serializer = UserLunchSerializer(queryset, many=True)
        return Response(serializer.data)


class HandleUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user:view_public_user_information_list"], ["user_lunch:get_all"]],
        "POST": [["user_lunch:edit"]],
        "PUT": [["user_lunch:edit"]],
        "DELETE": [["user_lunch:edit"]],
    }

    def get(self, request):
        user_lunches = UserLunchServices.get_users_lunch(profile=request.user.profile)
        serializer = UserLunchSerializer(user_lunches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                UserLunchServices.create(
                    serializer=serializer,
                    profile=request.user.profile,
                    date=request.data.get("date"),
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error_msg": str(e)})

    def get_object(self, pk):
        try:
            lunch = UserLunch.objects.get(id=pk)
            return lunch
        except UserLunch.DoesNotExist:
            return Response(dict(msg="Lunch not found"))

    def put(self, request, pk):
        serializer = UserLunchSerializer(
            instance=self.get_object(pk), data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            try:
                UserLunchServices.update(
                    serializer=serializer, pk=pk, date=request.data.get("date")
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"msg": str(e)})

    def delete(self, request, pk):
        try:
            UserLunchServices.delete(pk=pk)
            return Response(dict(msg="The lunch has been deleted"))
        except Exception as e:
            return Response({"msg": str(e)})


class HandleManyUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "POST": [["user_lunch:edit"]],
        "PUT": [["user_lunch:edit"]],
    }

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                list_dates = request.data.get("list_dates")
                profile = request.user.profile
                list_user_lunches = UserLunchServices.create_many(
                    data=serializer.validated_data,
                    profile=profile,
                    list_dates=list_dates,
                )
                day = "day" if len(list_user_lunches) <= 1 else "days"
                return Response(
                    dict(
                        msg=f"You have just created lunch for {len(list_user_lunches)} {day}"
                    )
                )
            except Exception as e:
                return Response({"error_msg": str(e)})

    def put(self, request):
        today = datetime.date.today()
        list_lunches = UserLunch.objects.filter(
            date__gt=today, profile=request.user.profile
        )
        if not list_lunches.exists():
            return Response(dict(msg="Don't have any lunches to delete"))
        list_lunches.delete()

        return Response(dict(msg="Deleted successfully all of lunches from now"))


class HandleUserLunchByAdmin(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "POST": [['user_lunch:edit_all_user_lunch']],
    }

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True, many=True)
        if serializer.is_valid(raise_exception=True):
            try:
                list_user_lunches = UserLunchServices.create_many_by_admin(
                    list_data=serializer.validated_data
                )
                return Response(
                    dict(
                        msg=f"You have just created lunch for {len(list_user_lunches)} user",
                        status=1
                    )
                    if len(list_user_lunches) else dict(
                        msg=f"Already registered",
                        status=0
                    )
                )
            except Exception as e:
                return Response({"error_msg": str(e)})

    def get_object(self, pk):
        try:
            lunch = UserLunch.objects.get(id=pk)
            return lunch
        except UserLunch.DoesNotExist:
            return Response(dict(msg="Lunch not found"))


class SetVeggieUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {} # type: dict

    def put(self, request):
        try:
            UserLunchServices.set_veggie(profile=request.user.profile)
            return Response(dict(msg="You have just set veggie lunch for this month"))
        except Exception as e:
            return Response({"msg": str(e)})


class CancelSetVeggieUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {} # type: dict

    def put(self, request):
        date = datetime.datetime.now()
        if date.hour >= Lunch.TIME_OUT:
            date += datetime.timedelta(days=1)
        user_lunches = UserLunch.objects.filter(
            date__gte=date, profile=request.user.profile, has_veggie=True
        ).update(has_veggie=False)
        data = {
            "msg": "Cancel veggie successfully" if user_lunches else "Don't have any veggie lunches to update"
        }
        return Response(data)


class AdminViewSet(ViewSet):
    queryset = UserLunch.objects.all()
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "update_many_veggie_for_employees": [["user_lunch:edit_all_user_lunch"]],
        "delete_many_for_employees": [["user_lunch:edit_all_user_lunch"]]
    }

    @action(methods=[HttpMethod.PUT], detail=False)
    def update_lunches(self, request):
        data_user_lunches = request.data.get("data_user_lunches")
        user_lunches = UserLunchServices.bulk_update_veggie(data_user_lunches=data_user_lunches)
        return Response(user_lunches)

    @action(methods=[HttpMethod.PUT], detail=False)
    def delete_lunches(self, request):
        user_lunch_ids = request.data.get("user_lunch_ids")
        user_lunches = UserLunchServices.bulk_delete(user_lunch_ids=user_lunch_ids)
        return Response(user_lunches)
