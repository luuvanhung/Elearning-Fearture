from api_oauth2.models import ApiKey, Application
from api_user.serializers.user import SmallUsersSerializer
from common.constants.api_oauth2 import ApplicationChoice
from oauth2_provider.settings import oauth2_settings

# from api_oauth2.pre_configured import get_scopes_backend
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from rest_framework.exceptions import ValidationError
from rest_framework.fields import BooleanField
from rest_framework.serializers import CharField, ModelSerializer, UUIDField


class ApplicationSerializer(ModelSerializer):
    user = SmallUsersSerializer()

    class Meta:
        model = Application
        fields = "__all__"


class SimpleApplicationSerializer(ModelSerializer):
    user = SmallUsersSerializer()

    class Meta:
        model = Application
        fields = [
            "id",
            "client_id",
            "name",
            "user",
            "client_type",
            "client_secret",
            "authorization_grant_type",
            "redirect_uris",
            "algorithm",
            "skip_authorization",
            "scope",
        ]


class ApplicationUpdateSerializer(ModelSerializer):
    name = CharField(max_length=255)
    client_type = CharField(max_length=32)
    authorization_grant_type = CharField(max_length=32)
    scopes = CharField(required=False, allow_blank=True)
    skip_authorization = BooleanField(required=False, default=False)
    algorithm = CharField(required=False, max_length=5, allow_blank=True, default="")
    user_id = UUIDField(required=False)

    class Meta:
        model = Application
        fields = [
            "name",
            "user_id",
            "client_type",
            "authorization_grant_type",
            "redirect_uris",
            "algorithm",
            "skip_authorization",
            "scope",
            "scopes",
        ]

    def validate(self, attrs):
        # name = attrs.get("name")
        client_type = attrs.get("client_type")
        authorization_grant_type = attrs.get("authorization_grant_type")
        algorithm = attrs.get("algorithm")
        # validate client_type
        if client_type not in ApplicationChoice.CLIENT_TYPES:
            raise ValidationError(
                {"client_type": "Client type must be confidential or public"}
            )
        # validate grant_type
        if authorization_grant_type not in ApplicationChoice.GRANT_TYPES:
            raise ValidationError(
                {"authorization_grant_type": "Grant type isn't support"}
            )
        # validate algorithm
        if algorithm not in ApplicationChoice.ALGORITHM_TYPES:
            raise ValidationError({"algorithm": "Algorithm isn't support"})
        return attrs


class ApplicationCreateSerializer(ModelSerializer):
    name = CharField(max_length=255)
    client_type = CharField(max_length=32)
    authorization_grant_type = CharField(max_length=32)
    scopes = CharField(required=False, allow_blank=True)
    skip_authorization = BooleanField(required=False, default=False)
    algorithm = CharField(required=False, max_length=5, allow_blank=True, default="")
    user_id = UUIDField(required=False)

    class Meta:
        model = Application
        fields = [
            "name",
            "user_id",
            "client_type",
            "authorization_grant_type",
            "redirect_uris",
            "algorithm",
            "skip_authorization",
            "scope",
            "scopes",
        ]

    def validate(self, attrs):
        name = attrs.get("name")
        client_type = attrs.get("client_type")
        authorization_grant_type = attrs.get("authorization_grant_type")
        algorithm = attrs.get("algorithm")

        # validate name
        name_exists = Application.objects.filter(name=name).exists()
        if name_exists:
            raise ValidationError({"name": "Application name is already exists"})
        # validate client_type
        if client_type not in ApplicationChoice.CLIENT_TYPES:
            raise ValidationError(
                {"client_type": "Client type must be confidential or public"}
            )
        # validate grant_type
        if authorization_grant_type not in ApplicationChoice.GRANT_TYPES:
            raise ValidationError(
                {"authorization_grant_type": "Grant type isn't support"}
            )
        # validate algorithm
        if algorithm not in ApplicationChoice.ALGORITHM_TYPES:
            raise ValidationError({"algorithm": "Algorithm isn't support"})
        return attrs


class ApplicationRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["scope"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Todo: use get_scopes_backend().get_available_scopes instead of
        if ret.get("scope") == "__all__":
            scopes = list(oauth2_settings.SCOPES)
            scopes_string = list_to_scope(scopes)
            ret.update(scope=scopes_string)
        return ret


class ApiKeySerializer(ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ["prefix", "name", "application_id"]
