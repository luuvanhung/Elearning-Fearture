from api_base.services import TokenUtil
from api_user.models import User
from api_user.models.titles import Titles
from api_user.serializers import ProfileSerializers
from api_user.services import UserService
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField


class UserRoleSerializer(serializers.Serializer):
    id = IntegerField(label="ID")
    name = CharField(max_length=200, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializers(required=False)
    roles = UserRoleSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "profile",
            "active",
            "admin",
            "title",
            "staff",
            "roles",
        )
        depth = 1

    def update(self, instance, validated_data):
        return UserService.update(instance, validated_data)


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = "__all__"

    def create(self, validate_data):
        return Titles.objects.create(**validate_data)


class SmallUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "title")


class UserVoteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField(source="profile.name")

    class Meta:
        model = User
        fields = ["id", "name"]


class UserReadSerializer(serializers.ModelSerializer):
    profile = ProfileSerializers(required=False)

    class Meta:
        model = User
        fields = ["id", "email", "profile"]
        depth = 1


class VerifyUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        payload = TokenUtil.verification_decode(data.get("token"))
        if not payload:
            raise serializers.ValidationError({"msg": "Invalid Token"})

        email = payload.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({"msg": "User not found"})

        if user.has_usable_password():
            raise serializers.ValidationError({"msg": "Your password has been setted"})

        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        email = TokenUtil.verification_decode(ret.get("token")).get("email")
        ret["email"] = email
        return ret


class UserIncludeNameAndTitleSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_title = serializers.SerializerMethodField()

    def get_user_name(self, instance):
        return instance.profile.name

    def get_user_title(self, instance):
        return instance.get_title()

    class Meta:
        model = User
        fields = ["id", "user_name", "user_title"]
