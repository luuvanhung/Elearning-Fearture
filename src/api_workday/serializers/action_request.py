from api_workday.models.request_detail import RequestDetail
from rest_framework import serializers

from .request_off import RequestOffSerializer


class RequestDetailSerializer(serializers.ModelSerializer):
    request_off = RequestOffSerializer(many=False, read_only=True)
    approver = serializers.SerializerMethodField("get_profile")

    @staticmethod
    def get_profile(obj):
        return {"id": obj.approve.id, "name": obj.approve.name, "email": obj.approve.user.email}

    class Meta:
        model = RequestDetail
        fields = "__all__"
