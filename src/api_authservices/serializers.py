from rest_framework import serializers


class GoogleSerializer(serializers.Serializer):
    sub = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, default="")
    last_name = serializers.CharField(required=False, default="")
    service = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password", "placeholder": "Password"}
    )
