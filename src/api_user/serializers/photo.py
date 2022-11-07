from api_user.models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "profile", "photo")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.update(photo=f'{ret.get("photo")}')
        return ret
