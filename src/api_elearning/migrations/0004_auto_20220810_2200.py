# Generated by Django 3.2.3 on 2022-08-10 22:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api_elearning', '0003_auto_20220803_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='next_chapter_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='short_des',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='cover_image',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='next_lesson_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='cover_image',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('course', 'title')},
        ),
    ]
