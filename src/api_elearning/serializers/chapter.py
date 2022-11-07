from api_elearning.models import Chapter, Course
from api_elearning.serializers import LessonReadSerializer, QuizSerializer
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers


class NextChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title']
        depth = 1


class ChapterSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Course.objects.all(),
                                                   source='course')
    lessons = LessonReadSerializer(many=True, required=False)
    previous_chapter = NextChapterSerializer(many=False, required=False)
    previous_chapter_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
                                                             write_only=True, queryset=Chapter.objects.all(),
                                                             source='previous_chapter')
    last_modifier = UserReadSerializer(required=False)
    last_modifier_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                          source='last_modifier')
    chapter_quizzes = QuizSerializer(many=True, required=False)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'lessons', 'previous_chapter_id', 'previous_chapter', 'course',
                  'course_id', 'chapter_quizzes', 'last_modifier', 'last_modifier_id']
        extra_kwargs = {
            'description': {'required': False},
            'title': {'required': False},
            'course': {'required': False}
        }
        depth = 1


class ChapterReadSerializer(serializers.ModelSerializer):
    lessons = LessonReadSerializer(many=True, required=False)
    last_modifier = UserReadSerializer(required=False)
    previous_chapter = NextChapterSerializer(many=False)
    chapter_quizzes = QuizSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'last_modifier', 'previous_chapter', 'lessons', 'chapter_quizzes']

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        lessons = instance.get('lessons')
        if lessons:
            lessons = [lesson for lesson in lessons if lesson]
            instance.update(lessons=lessons)
        return instance


class ChapterAttachmentSerializer(serializers.ModelSerializer):
    previous_chapter = NextChapterSerializer(many=False)
    chapter_quizzes = QuizSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'last_modifier_id', 'previous_chapter', 'chapter_quizzes']
