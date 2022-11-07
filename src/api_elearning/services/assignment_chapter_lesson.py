from datetime import date

from api_base.services import BaseService
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import AssignmentChapter, Lesson
from api_elearning.models.assignment import AssignmentChapterLesson
from api_elearning.services import AssignmentChapterService
from django.db.models import Q


class AssignmentChapterLessonService(BaseService):
    @classmethod
    def update_assignment_chapter_lesson(cls, instance, validated_data):
        if validated_data['status'] is AssignmentContentStatus.COMPLETED.value:
            next_lesson_ids = Lesson.objects.filter(previous_lesson_id=instance.lesson_id).values('id')
            obj_update = {
                'status': AssignmentContentStatus.OPEN.value,
                'start_date': date.today()
            }
            if next_lesson_ids:
                AssignmentChapterLesson.objects.filter(
                    Q(lesson_id__in=next_lesson_ids) & Q(assignment_chapter_id=instance.assignment_chapter_id)).update(
                    **obj_update)
            completed_lessons = AssignmentChapterLesson.objects.filter(
                Q(assignment_chapter_id=instance.assignment_chapter_id)).exclude(
                Q(status=AssignmentContentStatus.COMPLETED.value)).exclude(pk=instance.id)
            if not completed_lessons.exists():
                obj = AssignmentChapter.objects.filter(pk=instance.assignment_chapter_id).last()
                AssignmentChapterService.update_assignment_chapter(obj,
                                                                   {'status': AssignmentContentStatus.COMPLETED.value})
        AssignmentChapterLesson.objects.filter(pk=instance.id).update(**validated_data, end_date=date.today())
        return AssignmentChapterLesson(id=instance.id, **validated_data)
