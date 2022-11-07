from api_elearning.models import Attachment, Lesson
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers
from rest_framework.fields import UUIDField


class AttachmentSerializer(serializers.ModelSerializer):
    owner = UserReadSerializer(required=False, many=False)
    owner_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                  source='owner')
    lesson_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Lesson.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='lesson')

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'lesson_id', 'lesson', 'mine_type', 'length', 'original_name', 'path', 'owner_id',
                  'owner', 'forced_read']
        extra_kwargs = {
            'lesson': {'required': False, 'write_only': True},
            'path': {'write_only': True},
        }


class AttachmentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'mine_type', 'length', 'original_name', 'forced_read']
