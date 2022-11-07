from api_wfh.models.wfh_request import WfhRequest
from api_wfh.serializers.wfh_date import WfhDateSerializer
from rest_framework import serializers


class WfhRequestSerializer(serializers.ModelSerializer):
    wfh_date = WfhDateSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField("get_user")

    def get_user(self, obj):
        return {"id": obj.user.profile.id, "name": obj.user.profile.name, "email": obj.user.profile.personal_email}

    class Meta:
        model = WfhRequest
        fields = "__all__"
        read_only_fields = ["user"]
