from datetime import date

from api_base.services import BaseService
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import Assignment, AssignmentChapter, AssignmentChapterLesson, Chapter
from django.db.models import Q


class AssignmentChapterService(BaseService):
    @classmethod
    def update_assignment_chapter(cls, instance, validated_data):
        if validated_data['status'] is AssignmentContentStatus.COMPLETED.value:
            next_chapter_ids = Chapter.objects.filter(previous_chapter_id=instance.chapter_id).values('id')
            obj_update = {
                'status': AssignmentContentStatus.OPEN.value,
                'start_date': date.today()
            }
            if next_chapter_ids:
                AssignmentChapter.objects.filter(
                    Q(chapter_id__in=next_chapter_ids) & Q(assignment_id=instance.assignment_id)).update(**obj_update)

                AssignmentChapterLesson.objects.filter(
                    Q(assignment_chapter_id=instance.id) & Q(lesson__previous_lesson=None)).update(
                    status=AssignmentContentStatus.OPEN.value)
            completed_chapters = AssignmentChapter.objects.filter(
                Q(assignment_id=instance.assignment_id)).exclude(
                Q(status=AssignmentContentStatus.COMPLETED.value)).exclude(pk=instance.id)
            if not completed_chapters.exists():
                Assignment.objects.filter(pk=instance.assignment_id).update(
                    status=AssignmentContentStatus.COMPLETED.value)
        AssignmentChapter.objects.filter(pk=instance.id).update(**validated_data, end_date=date.today())
        return AssignmentChapter(id=instance.id, **validated_data)
