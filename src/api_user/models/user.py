import uuid

from api_base.manager import UserManager
from api_user.models import Titles
from api_user.models.roles import Role
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    password = models.CharField(verbose_name="password", max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True)
    active = models.BooleanField(default=True)
    title = models.ManyToManyField(Titles, related_name="users", null=True, blank=True)
    staff = models.BooleanField(default=False)  # staff not superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField(Role, related_name="users", null=True)
    USERNAME_FIELD = "email"  # username

    objects = UserManager()

    class Meta:
        db_table = "hr_users"

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    def set_password(self, raw_password):
        self.password = make_password(password=raw_password, salt=settings.SECRET_KEY)
        self._password = raw_password

    @property
    def user_profile(self):
        from api_user.models import Profile

        # noinspection PyUnresolvedReferences
        return Profile.objects.filter(id=self.profile.id)

    def get_title(self):
        return " ,".join([title.title for title in self.title.all()])
