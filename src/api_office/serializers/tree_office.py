from api_office.models import Department, Group, Office
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    manager_name = serializers.SerializerMethodField()
    manager_title = serializers.SerializerMethodField()

    def get_avatar(self, instance):
        if instance.manager is None:
            return None
        else:
            return (
                str(instance.manager.profile.image)
                if instance.manager.profile.image
                else None
            )

    def get_manager_name(self, instance):
        return instance.manager.profile.name if instance.manager else None

    def get_manager_title(self, instance):
        return instance.manager.get_title() if instance.manager else None

    class Meta:
        abstract = True


class GetDepartmentserializer(BaseSerializer):
    class Meta:
        model = Department
        fields = ["id", "manager_id", "name", "avatar", "manager_name", "manager_title"]


class GetGroupserializer(BaseSerializer):
    class Meta:
        model = Group
        fields = ["id", "manager_id", "name", "avatar", "manager_name", "manager_title"]


class QuerysetOfficeSerializer(BaseSerializer):
    class Meta:
        model = Office
        fields = ["id", "manager_id", "name", "avatar", "manager_name", "manager_title"]
