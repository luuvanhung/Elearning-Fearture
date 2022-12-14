# Generated by Django 3.2.3 on 2022-09-14 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_elearning', '0016_add_record_in_question_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentchapterlesson',
            name='quiz_result',
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='lesson_name',
        ),
        migrations.RemoveField(
            model_name='quizresultdetail',
            name='content',
        ),
        migrations.AddField(
            model_name='assignmentchapterlesson',
            name='completed_lesson_content',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='responser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='assignment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='quiz_results', to='api_elearning.assignment'),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='assignment_chapter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='quiz_results', to='api_elearning.assignmentchapter'),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='assignment_chapter_lesson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='quiz_results', to='api_elearning.assignmentchapterlesson'),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='is_passed',
            field=models.BooleanField(default=False),
        ),
    ]
