import uuid

from api_base.models import TimeStampedModel
from api_elearning.models import Chapter, Course, Lesson, QuestionType
from api_user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Quiz(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    threshold = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], )
    lesson = models.ForeignKey(Lesson, related_name="lesson_quizzes", blank=True, null=True, on_delete=models.SET_NULL,
                               default=None)
    chapter = models.ForeignKey(Chapter, related_name="chapter_quizzes", blank=True, null=True,
                                on_delete=models.SET_NULL, default=None)
    course = models.ForeignKey(Course, related_name="course_quizzes", blank=True, null=True, on_delete=models.SET_NULL,
                               default=None)
    shuffled = models.BooleanField(default=False)
    responser = models.ForeignKey(User, related_name="quizzes", blank=True, null=True, on_delete=models.SET_NULL,
                                  default=None)

    class Meta:
        db_table = "el_quizzes"
        ordering = ["created_at"]


class Question(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_questions")
    content = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=1)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name="type_questions")
    order = models.IntegerField(default=0)

    class Meta:
        db_table = "el_questions"
        ordering = ('order', 'quiz')


class Answer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_answers")
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = "el_answers"
        ordering = ('order', 'question')
