import uuid

from api_elearning.models import Chapter, Lesson
from api_elearning.serializers import AttachmentReadSerializer, QuizSerializer
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers


class NextLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']
        depth = 1


class LessonSerializer(serializers.ModelSerializer):
    attachments = AttachmentReadSerializer(many=True, read_only=True)
    last_modifier = UserReadSerializer(required=False)
    last_modifier_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                          source='last_modifier')
    chapter_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Chapter.objects.all(),
                                                    source='chapter')
    previous_lesson = NextLessonSerializer(many=False, required=False)
    previous_lesson_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
                                                            write_only=True, queryset=Lesson.objects.all(),
                                                            source='previous_lesson')

    # next
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'previous_lesson', 'previous_lesson_id', 'attachments', 'chapter_id',
                  'chapter',
                  'last_modifier', 'last_modifier_id']
        extra_kwargs = {
            'previous_lesson': {'required': False},
            'title': {'required': False},
            'content': {'required': False},
            'chapter': {'required': False},
        }
        depth = 1


class LessonReadSerializer(serializers.ModelSerializer):
    attachments = AttachmentReadSerializer(many=True, read_only=True)
    last_modifier = UserReadSerializer(required=False, read_only=True)
    previous_lesson = NextLessonSerializer(many=False)
    lesson_quizzes = QuizSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'previous_lesson', 'last_modifier',
                  'attachments', 'lesson_quizzes']
        depth = 1

    def to_representation(self, instance):
        context = self.context
        instance = super().to_representation(instance)
        if context.get('view') and context.get('view').action in ['retrieve']:
            if not instance.get('title'):
                if context.get('request').user.id.hex == uuid.UUID(instance.get('last_modifier').get('id')).hex:
                    Lesson.objects.filter(pk=instance.get('id')).delete()
                return None
        return instance
