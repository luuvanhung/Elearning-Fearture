import uuid
from django.db.models import Q

from api_base.models import TimeStampedModel
from api_elearning.constants.status import AssignmentContentStatus
from api_elearning.models import (
    Answer,
    Assignment,
    AssignmentChapter,
    AssignmentChapterLesson,
    Question,
    QuestionType,
    Quiz,
)
from api_user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class QuizResult(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    quiz = models.ForeignKey(Quiz, related_name="quiz_results", blank=True, null=True, on_delete=models.SET_NULL,
                             default=None)
    quiz_title = models.CharField(max_length=255)
    threshold = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], )
    user = models.ForeignKey(User, related_name="quiz_results", blank=True, null=True, on_delete=models.SET_NULL,
                             default=None)
    full_name = models.CharField(max_length=255)
    assignment = models.ForeignKey(Assignment, related_name="quiz_results", blank=True, null=True,
                                   on_delete=models.SET_NULL, default=None)
    assignment_chapter = models.ForeignKey(AssignmentChapter, related_name="quiz_results", blank=True, null=True,
                                           on_delete=models.SET_NULL, default=None)
    assignment_chapter_lesson = models.ForeignKey(AssignmentChapterLesson, related_name="quiz_results", blank=True,
                                                  null=True, on_delete=models.SET_NULL, default=None)
    is_passed = models.BooleanField(default=False)
    submit_at = models.DateTimeField(default=timezone.now)
    CREATE_AT_FIELD = "submit_at"

    class Meta:
        db_table = "el_quiz_results"
        ordering = ["-submit_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_passed:
            if self.assignment_chapter_id:
                assignment_chapter = AssignmentChapter.objects.get(id=self.assignment_chapter_id)
                remaining_lessons = AssignmentChapterLesson.objects.filter(
                    Q(assignment_chapter_id=self.assignment_chapter_id))
                remaining_lessons = [lesson for lesson in remaining_lessons
                                     if lesson.status != AssignmentContentStatus.COMPLETED.value]
                remaining_quizzes = QuizResult.objects.filter(
                    Q(assignment_chapter_id=self.assignment_chapter_id))
                remaining_quizzes = [quiz for quiz in remaining_quizzes if not quiz.is_passed]
                if not remaining_lessons and not remaining_quizzes:
                    assignment_chapter.status = AssignmentContentStatus.COMPLETED.value
                    assignment_chapter.save()


class QuizResultDetail(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    score = models.IntegerField(default=1)
    question = models.ForeignKey(Question, related_name="quiz_result_details", blank=True, null=True,
                                 on_delete=models.SET_NULL, default=None)
    question_content = models.CharField(max_length=255)
    type = models.ForeignKey(QuestionType, related_name="type_result_details", on_delete=models.CASCADE)
    quiz_result = models.ForeignKey(QuizResult, related_name="quiz_result_details", on_delete=models.CASCADE)

    class Meta:
        db_table = "el_quiz_result_details"
        ordering = ["-created_at"]


class QuizResultDetailAnswer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    answer_content = models.CharField(max_length=255)
    answer = models.ForeignKey(Answer, related_name="quiz_result_detail_answers", blank=True, null=True,
                               on_delete=models.SET_NULL, default=None)
    correct = models.BooleanField(default=False)
    chosen = models.BooleanField(default=False)
    quiz_result_detail = models.ForeignKey(QuizResultDetail, related_name="quiz_result_detail_answers",
                                           on_delete=models.CASCADE)
    user_response = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "el_quiz_result_detail_answers"
        ordering = ["-created_at"]
