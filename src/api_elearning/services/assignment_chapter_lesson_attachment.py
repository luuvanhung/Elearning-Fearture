from datetime import date

from api_base.services import BaseService
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import AssignmentChapterLesson, AssignmentChapterLessonAttachment
from api_elearning.services import AssignmentChapterLessonService
from django.db.models import Q


class AssignmentChapterLessonAttachmentService(BaseService):
    @classmethod
    def update_assignment_attachment(cls, instance, validated_data):
        if validated_data['read'] and instance.attachment.forced_read:
            remaining_attachments = AssignmentChapterLessonAttachment.objects.filter(
                Q(assignment_chapter_lesson_id=instance.assignment_chapter_lesson_id)).exclude(
                Q(read=True)).exclude(pk=instance.id)
            remaining_forced_read_attachments = [attachment for attachment in remaining_attachments
                                                 if attachment.attachment.forced_read]
            if not len(remaining_forced_read_attachments):
                obj = AssignmentChapterLesson.objects.filter(pk=instance.assignment_chapter_lesson_id).last()
                AssignmentChapterLessonService.update_assignment_chapter_lesson(obj, {
                    'status': AssignmentContentStatus.COMPLETED.value})
        AssignmentChapterLessonAttachment.objects.filter(pk=instance.id).update(**validated_data, end_date=date.today())
        return AssignmentChapterLessonAttachment(id=instance.id, **validated_data)
