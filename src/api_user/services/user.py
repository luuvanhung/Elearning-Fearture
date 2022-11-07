import datetime
from typing import Any, List, Tuple

from api_authservices.models import AuthenticationProvider, LinkingAccount
from api_base.services import BaseService, SendMail, TokenUtil
from api_office.models import Office
from api_team.models import TeamMembers
from api_user.models import Profile, User, Titles
from api_user.models.roles import Role
from api_workday.services.remain_leave import RemainLeaveService
from common.constants.workday_constants import Workday
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate
from django.template.loader import render_to_string


class UserService(BaseService):
    @classmethod
    def get_filter_query(cls, request):
        query_name_or_email = request.query_params.get('name_or_email')
        query_gender = request.query_params.get("gender")
        query_title = request.query_params.get("title")
        query_team = request.query_params.get("team")
        query_birthday = request.query_params.get("birthday")
        query_joindate = request.query_params.get("joindate")
        query_active = request.query_params.get("active")
        filter_args = dict()  # type: dict
        if query_gender is not None and query_gender != "":
            filter_args.update(profile__gender__istartswith=query_gender)
        if query_team not in (None, "", "All", "all"):
            members = (
                TeamMembers.objects.select_related("team")
                .filter(team__team_name=query_team)
                .values_list("member_id", flat=True)
            )
            filter_args.update(id__in=members)
        if query_title:
            filter_args.update(title__id=query_title)
        if query_birthday is not None and query_birthday != "":
            filter_args.update(profile__birth_day__month=query_birthday)
        if query_joindate:
            query_joindate = datetime.datetime.strptime(query_joindate, "%Y-%m")
            filter_args.update(
                profile__join_date__month=query_joindate.month,
                profile__join_date__year=query_joindate.year,
            )
        if query_active is not None:
            filter_args.update(active=query_active)

        queryset = User.objects.select_related("profile").filter(**filter_args).order_by('profile')
        if query_name_or_email:
            queryset = queryset.filter(Q(profile__name__icontains=Collate(
                Value(query_name_or_email.strip()), "utf8mb4_general_ci"
            )) | Q(email__icontains=query_name_or_email.strip()))
        return queryset

    @classmethod
    def import_users(cls, users: dict, base_link="{settings.UI_HOST}/verify"):
        list_users = []
        list_profiles = []
        office = Office.objects.all().first()
        remain_leave = Workday.DEFAULT_ANNUAL_DAY
        valid_user, invalid_user = cls.separation_data(users)
        with transaction.atomic():
            for item in valid_user:
                email = item.get("email")
                name = item.get("name")
                phone = item.get("phone")
                join_date = item.get("join_date")
                user = User(email=email, password="123456", active=True, staff=False, admin=False)
                profile = Profile(
                    user=user,
                    name=name,
                    phone=phone,
                    personal_email=email,
                    join_date=datetime.datetime.strptime(join_date,
                                                         '%Y-%m-%d') if join_date else datetime.datetime.now(),
                    office=office,
                )
                token = TokenUtil.verification_encode(name, email, phone, personal_email=None)
                link = f"{base_link}?token={token}"
                content = render_to_string(
                    "../templates/invitation_email.html",
                    {"name": name, "email": email, "link": link, "token": token},
                )
                SendMail.start(
                    [email], "Welcome to Company Management", content
                )
                list_users.append(user)
                list_profiles.append(profile)

            User.objects.bulk_create(list_users)
            Profile.objects.bulk_create(list_profiles)
            for profile in list_profiles:
                RemainLeaveService.create_annual_leave(
                    current_date=datetime.datetime.now(), profile=profile, remain_leave=remain_leave
                )

        for item in valid_user:
            email = item.get("email")
            user = User.objects.filter(email=email).first()
            if item.get("title"):
                titles = item.get("title").split("/")
                list_roles = [Titles.objects.filter(title=title).first() for title in titles]
                user.title.set(list_roles)
                user.save()

        return valid_user, invalid_user

    @classmethod
    def separation_data(cls, data: dict) -> Tuple[List[Any], List[Any]]:
        valid_user = []
        valid_email = []
        invalid_user = []
        for user in data:
            email = user.get("email")
            if email in valid_email:
                user.update({"status": "Duplicate email in list"})
                invalid_user.append(user)
            else:
                valid_user.append(user)
                valid_email.append(user.get("email"))

        return valid_user, invalid_user

    @classmethod
    def get_list_emails_by_ids(cls, user_ids: list):
        return list(
            User.objects.filter(pk__in=user_ids)
            .order_by("email")
            .values_list("email", flat=True)
            .distinct()
        )

    @classmethod
    def get_user_by_id(cls, pk):
        user = User.objects.filter(pk=pk).first()
        return user

    @classmethod
    def get_user_by_email(cls, email):
        user = User.objects.filter(email=email).first()
        return user

    @classmethod
    def activate_user(cls, user):
        user.active = True
        user.save()

    @classmethod
    def deactivate_user(cls, user):
        user.active = False
        user.save()

    @classmethod
    def update_password(cls, data, user):
        """Update new password for user

        Parameters
        -------
        @param data: data requested, it must contain current_password and new_password
        @param user: user information needs to be changed

        Returns
        -------
        error_message: str
            we will set string value for error_message and set updated_user is None if have any error when we check data
            before changing password
        """
        message_error = None

        current_password = data.get("current_password", None)
        if not current_password:
            message_error = "Requested current password is not exist"
            return message_error

        hash_password = make_password(
            password=current_password, salt=settings.SECRET_KEY
        )
        if user.password != hash_password:
            message_error = "Password does not match"
            return message_error
        user.set_password(data.get("new_password"))
        return message_error

    @classmethod
    def invite(cls, email, name, base_link="{settings.UI_HOST}/verify"):
        cls.send_mail(email=email, name=name, send_email=True, base_link=base_link)
        return {"success": True, "user": {"name": name, "email": email}}

    @classmethod
    def send_mail(
        cls,
        email=None,
        name=None,
        phone=None,
        join_date=None,
        remain_leave=Workday.DEFAULT_ANNUAL_DAY,
        personal_email=None,
        send_email=False,
        base_link="",
    ):
        if send_email:
            token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}?token={token}"
            content = render_to_string(
                "../templates/invitation_email.html",
                {"name": name, "email": email, "link": link, "token": token},
            )
            SendMail.start(
                [email, personal_email], "Welcome to Company Management", content
            )
        if phone == "":
            phone = None
        with transaction.atomic():
            user = User.objects.create_user(email=email, password="123456")
            user.set_unusable_password()
            user.save()
            office = Office.objects.all().first()
            profile = Profile.objects.create(
                user=user,
                name=name,
                phone=phone,
                personal_email=email,
                join_date=join_date if join_date else datetime.datetime.now(),
                office=office,
            )
            RemainLeaveService.create_annual_leave(
                current_date=datetime.datetime.now(), profile=profile, remain_leave=remain_leave
            )

    @classmethod
    def update(cls, instance, validated_data):
        roles = ""
        if "roles" in validated_data:
            roles = validated_data.pop("roles")
        User.objects.filter(pk=instance.id).update(**validated_data)
        if roles:
            roles_list = []
            role_id_list = map(lambda t: t.get("id"), roles)
            roles_list.extend(Role.objects.in_bulk(role_id_list))
            instance.roles.set(roles_list)
        else:
            instance.roles.set([])
        return instance

    @classmethod
    @transaction.atomic
    def check_account_linking(
        cls,
        *,
        sub: str,
        email: str,
        first_name: str,
        last_name: str,
        iss: str,
        **extra_data,
    ):

        linking_account = LinkingAccount.objects.filter(account_id=sub).first()
        if linking_account:
            user = linking_account.user
            return user, True
        else:
            user = User.objects.filter(email=email).first()
            if user is None:
                return None, False
            service_provider = AuthenticationProvider.objects.filter(
                service_name=iss
            ).first()
            LinkingAccount.objects.create(
                user=user, service_provider=service_provider, account_id=sub
            )
            return user, True

    @classmethod
    def set_password(cls, email=None, password=None):
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
