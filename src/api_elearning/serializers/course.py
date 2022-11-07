from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import Assignment, AssignmentChapter, Course, Topic
from api_elearning.serializers import ChapterReadSerializer, QuizSerializer, TopicTitleSerializer
from api_user.models import User
from api_user.serializers import UserReadSerializer
from rest_framework import serializers
from rest_framework.fields import UUIDField


class CourseSerializer(serializers.ModelSerializer):
    topics = TopicTitleSerializer(many=True, required=False)
    instructor = UserReadSerializer(required=False)
    instructor_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='instructor')
    topic_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Topic.objects.all(), pk_field=UUIDField(format='hex'),
                                                   source='topics')
    chapters = ChapterReadSerializer(many=True, required=False)
    course_quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'short_des', 'instructor', 'instructor_id', 'cover_image', 'topics',
                  'topic_ids', 'created_at', 'updated_at', 'chapters', 'course_quizzes']
        extra_kwargs = {
            'title': {'required': False},
        }

    def update(self, instance, validated_data):
        topics = validated_data.get('topics')
        if topics is not None:
            instance.topics.set(topics)
            del validated_data['topics']
        else:
            instance.topics.clear()
        instance = super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        topics = validated_data.get('topics')
        if topics is not None:
            del validated_data['topics']
        course = Course.objects.create(**validated_data)
        course.topics.set(topics)
        return course

    def to_representation(self, instance):
        context = self.context.get('view')

        if context and context.action in ['get_my_assignments']:
            assignment_id = instance.assignment_id
            assignment = Assignment.objects.get(id=assignment_id)
            assignment_chapters = AssignmentChapter.objects.filter(assignment_id=assignment_id)
            instance = super().to_representation(instance)
            lesson_counter = attachment_counter = 0
            for chapter in instance['chapters']:
                lesson_counter += len(chapter['lessons'])
                for lesson in chapter['lessons']:
                    attachment_counter += len(lesson['attachments'])

            instance['assignment'] = {
                'assigned_at': assignment.created_at,
                'start_date': assignment.start_date,
                'end_date': assignment.end_date,
                'due_date': assignment.due_date,
                'status': assignment.status,
                'number_of_completed_chapters': len(
                    [assignment_chapter.id for assignment_chapter in assignment_chapters
                     if assignment_chapter.status == AssignmentContentStatus.COMPLETED.value])
            }
            instance['assignment_id'] = str(assignment_id)
            instance['number_of_chapters'] = len(instance['chapters'])
            instance['number_of_lessons'] = lesson_counter
            instance['number_of_attachments'] = attachment_counter
        elif context and context.action in ['get_assigned_course']:
            lesson_counter = 0
            for chapter in instance['chapters']:
                lesson_counter = lesson_counter + len(chapter['lessons'])
            instance['chapters'] = len(instance['chapters'])
            instance['lessons'] = lesson_counter
        else:
            instance = super().to_representation(instance)

        return instance


class CourseListSerializer(serializers.ModelSerializer):
    topics = TopicTitleSerializer(many=True)
    instructor = UserReadSerializer()
    course_quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'short_des', 'instructor', 'cover_image', 'topics',
                  'created_at', 'updated_at', 'course_quizzes']
