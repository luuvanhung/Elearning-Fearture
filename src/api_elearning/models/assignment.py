import uuid

from api_base.models import TimeStampedModel
from api_elearning.constants import AssignmentStatus
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import Attachment, Chapter, Course, Lesson
from api_user.models import User
from django.db import models
from django.db.models import Q


class Assignment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    full_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    course_name = models.CharField(max_length=255)
    status = models.CharField(choices=AssignmentStatus.choices(), default=AssignmentStatus.OPEN.value, max_length=50)

    class Meta:
        db_table = "el_assignments"
        ordering = ["created_at"]


class AssignmentChapter(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="assignment_chapters")
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="assignment_chapters")
    chapter_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=AssignmentContentStatus.choices(), default=AssignmentContentStatus.LOCK.value,
                              max_length=50)
    previous_assignment_chapter_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        assignment = Assignment.objects.get(pk=self.assignment_id)
        if assignment.status == AssignmentContentStatus.OPEN.value and \
                self.status != AssignmentContentStatus.OPEN.value and self.status != AssignmentContentStatus.LOCK.value:
            assignment.status = AssignmentContentStatus.IN_PROGRESS.value
            assignment.save()

        if self.status == AssignmentContentStatus.COMPLETED.value:
            following_assignment_chapters = AssignmentChapter.objects.filter(
                previous_assignment_chapter_id=self.id
            )
            if following_assignment_chapters:
                for following_assignment_chapter in following_assignment_chapters:
                    if following_assignment_chapter.status == AssignmentContentStatus.LOCK.value:
                        following_assignment_chapter.status = AssignmentContentStatus.OPEN.value
                        following_assignment_chapter.save()

            remaining_chapters = AssignmentChapter.objects.filter(
                Q(assignment_id=self.assignment_id))
            remaining_chapters = [chapter for chapter in remaining_chapters
                                  if chapter.status != AssignmentStatus.COMPLETED.value]
            if not remaining_chapters:
                assignment.status = AssignmentContentStatus.COMPLETED.value
                assignment.end_date = self.updated_at
                assignment.save()

    class Meta:
        db_table = "el_assignment_chapters"
        ordering = ["created_at"]


class AssignmentChapterLesson(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assignment_chapter = models.ForeignKey(AssignmentChapter, on_delete=models.CASCADE,
                                           related_name="assignment_chapter_lessons")
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="assignment_chapter_lessons")
    lesson_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=AssignmentContentStatus.choices(), default=AssignmentContentStatus.LOCK.value,
                              max_length=50)
    completed_lesson_content = models.BooleanField(default=False)
    previous_assignment_chapter_lesson_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        assignment_chapter = AssignmentChapter.objects.get(pk=self.assignment_chapter_id)

        if assignment_chapter.status == AssignmentContentStatus.OPEN.value and \
                self.status != AssignmentContentStatus.OPEN.value and self.status != AssignmentContentStatus.LOCK.value:
            assignment_chapter.status = AssignmentContentStatus.IN_PROGRESS.value
            assignment_chapter.save()

        if self.status == AssignmentContentStatus.COMPLETED.value:
            following_assignment_chapter_lessons = AssignmentChapterLesson.objects.filter(
                previous_assignment_chapter_lesson_id=self.id
            )
            if following_assignment_chapter_lessons:
                for following_assignment_chapter_lesson in following_assignment_chapter_lessons:
                    if following_assignment_chapter_lesson.status == AssignmentContentStatus.LOCK.value:
                        following_assignment_chapter_lesson.status = AssignmentContentStatus.OPEN.value
                        following_assignment_chapter_lesson.save()

            remaining_lessons = AssignmentChapterLesson.objects.filter(
                Q(assignment_chapter_id=self.assignment_chapter_id)
            )
            remaining_lessons = [lesson for lesson in remaining_lessons
                                 if lesson.status != AssignmentStatus.COMPLETED.value]
            if not remaining_lessons:
                assignment_chapter.status = AssignmentContentStatus.COMPLETED.value
                assignment_chapter.end_date = self.updated_at
                assignment_chapter.save()

    class Meta:
        db_table = "el_assignment_chapter_lessons"
        ordering = ["created_at"]


class AssignmentChapterLessonAttachment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assignment_chapter_lesson = models.ForeignKey(AssignmentChapterLesson, on_delete=models.CASCADE,
                                                  related_name="assignment_chapter_lesson_attachments")
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, related_name="assignment_attachments")
    current_time = models.TimeField(blank=True, null=True)
    current_page = models.IntegerField(blank=True, null=True)
    read = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.read:
            self.end_date = self.updated_at
        super().save(*args, **kwargs)
        assignment_chapter_lesson = AssignmentChapterLesson.objects.get(pk=self.assignment_chapter_lesson_id)

        if assignment_chapter_lesson.status == AssignmentContentStatus.OPEN.value \
                and (self.current_page or self.current_time):
            assignment_chapter_lesson.status = AssignmentContentStatus.IN_PROGRESS.value
            assignment_chapter_lesson.save()

        if self.read and self.attachment.forced_read:
            remaining_attachments = AssignmentChapterLessonAttachment.objects.filter(
                Q(assignment_chapter_lesson_id=self.assignment_chapter_lesson_id)).exclude(
                Q(read=True)).exclude(pk=self.id)
            remaining_forced_read_attachments = [attachment for attachment in remaining_attachments
                                                 if attachment.attachment.forced_read]
            if not remaining_forced_read_attachments:
                assignment_chapter_lesson.status = AssignmentContentStatus.COMPLETED.value
                assignment_chapter_lesson.end_date = self.updated_at
                assignment_chapter_lesson.save()

    class Meta:
        db_table = "el_assignment_chapter_lesson_attachments"
        ordering = ["created_at"]
