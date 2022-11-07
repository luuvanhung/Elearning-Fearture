from api_wfh.models.wfh_date import WfhDate
from rest_framework import serializers


class WfhDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WfhDate
        fields = "__all__"
