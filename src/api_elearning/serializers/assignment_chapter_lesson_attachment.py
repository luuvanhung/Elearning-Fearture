from rest_framework import serializers
from rest_framework.fields import UUIDField

from api_elearning.models import AssignmentChapterLessonAttachment, Attachment
from api_elearning.serializers import AttachmentReadSerializer


class AssignmentChapterLessonAttachmentSerializer(serializers.ModelSerializer):
    assignment_chapter_lesson_id = serializers.PrimaryKeyRelatedField(required=False,
                                                                      queryset=AssignmentChapterLessonAttachment.objects.all(),
                                                                      pk_field=UUIDField(format='hex'),
                                                                      source='assignment_chapter_lesson')
    attachment_id = serializers.PrimaryKeyRelatedField(required=False,
                                                       queryset=Attachment.objects.all(),
                                                       pk_field=UUIDField(format='hex'),
                                                       source='attachment',
                                                       write_only=True)
    attachment = AttachmentReadSerializer(required=False, read_only=True)

    class Meta:
        model = AssignmentChapterLessonAttachment
        fields = ['id', 'assignment_chapter_lesson_id', 'attachment_id', 'attachment', 'start_date', 'end_date', 'read',
                  'current_time', 'current_page']
        extra_kwargs = {
            'ended': {'required': False},
            'current_page': {'required': False},
            'current_time': {'required': False},
        }
