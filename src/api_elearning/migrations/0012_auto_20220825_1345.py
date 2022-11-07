# Generated by Django 3.2.3 on 2022-08-25 13:45

from re import T
import uuid

import django.core.validators
import django.utils.timezone
from api_elearning.constants.status import AssignmentContentStatus, AssignmentStatus
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_elearning', '0011_auto_20220824_0507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'el_answers',
                'ordering': ('order', 'question'),
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('due_date', models.DateTimeField(null=True, blank=True)),
                ('course_name', models.CharField(max_length=255)),
                ('status', models.CharField(
                    choices=AssignmentStatus.choices(), default=AssignmentStatus.OPEN.value, max_length=50)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='assignments', to='api_elearning.course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                        related_name='assignments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'el_assignments',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='AssignmentChapter',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('chapter_name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(
                    choices=AssignmentContentStatus.choices(), default=AssignmentContentStatus.LOCK.value,
                    max_length=50)),
                ('assignment',
                models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_chapters',
                                to='api_elearning.assignment')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='assignment_chapters', to='api_elearning.chapter')),
            ],
            options={
                'db_table': 'el_assignment_chapters',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=1)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'el_questions',
                'ordering': ('order', 'quiz'),
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'el_question_types',
                'ordering': ['created_at'],
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('threshold', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0),
                                                            django.core.validators.MaxValueValidator(1.0)])),
                ('shuffled', models.BooleanField(default=False)),
                ('chapter',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='chapter_quizzes', to='api_elearning.chapter')),
                ('course',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='course_quizzes', to='api_elearning.course')),
                ('lesson',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='lesson_quizzes', to='api_elearning.lesson')),
            ],
            options={
                'db_table': 'el_quizzes',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quiz_title', models.CharField(max_length=255)),
                ('threshold', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0),
                                                            django.core.validators.MaxValueValidator(1.0)])),
                ('full_name', models.CharField(max_length=255)),
                ('lesson_name', models.CharField(max_length=255)),
                ('submit_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('lesson',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='quiz_results', to='api_elearning.lesson')),
                ('quiz',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='quiz_results', to='api_elearning.quiz')),
                ('user',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='quiz_results', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'el_quiz_results',
                'ordering': ['-submit_at'],
            },
        ),
        migrations.CreateModel(
            name='QuizResultDetail',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=1)),
                ('question_content', models.CharField(max_length=255)),
                ('question',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='quiz_result_details', to='api_elearning.question')),
                ('quiz_result',
                models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_result_details',
                                to='api_elearning.quizresult')),
                ('type',
                models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_result_details',
                                to='api_elearning.questiontype')),
            ],
            options={
                'db_table': 'el_quiz_result_details',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuizResultDetailAnswer',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('answer_content', models.CharField(max_length=255)),
                ('correct', models.BooleanField(default=False)),
                ('chosen', models.BooleanField(default=False)),
                ('user_response', models.TextField(blank=True, null=True)),
                ('answer',
                models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                related_name='quiz_result_detail_answers', to='api_elearning.answer')),
                ('quiz_result_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                        related_name='quiz_result_detail_answers',
                                                        to='api_elearning.quizresultdetail')),
            ],
            options={
                'db_table': 'el_quiz_result_detail_answers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_questions',
                                    to='api_elearning.quiz'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_questions',
                                    to='api_elearning.questiontype'),
        ),
        migrations.CreateModel(
            name='AssignmentChapterLesson',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id',
                models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('lesson_name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(
                    choices=AssignmentContentStatus.choices(), default=AssignmentContentStatus.LOCK.value,
                    max_length=50)),
                ('assignment_chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                        related_name='assignment_chapter_lessons',
                                                        to='api_elearning.assignmentchapter')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='assignment_chapter_lessons', to='api_elearning.lesson')),
                ('quiz_result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                related_name='assignment_chapter_lessons',
                                                to='api_elearning.quizresult')),
            ],
            options={
                'db_table': 'el_assignment_chapter_lessons',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers',
                                    to='api_elearning.question'),
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='next_chapter',
            new_name='previous_chapter',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='next_lesson',
            new_name='previous_lesson',
        ),
    ]
