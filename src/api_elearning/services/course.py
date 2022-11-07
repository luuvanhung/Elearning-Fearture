from uuid import UUID

from django.db.models import Q

from api_base.services import BaseService
from api_elearning.models import Course
from api_user.models import User


class CourseService(BaseService):
    @classmethod
    def get_status(cls, course_id, user_id):
        sql = """
            SELECT
                hr_chapters.id,
                hr_chapters.title as chapter_title,
                hr_lessons.id as lesson_id,
                hr_lessons.title as lesson_title,
                hr_user_lessons.status
            FROM
                hr_courses
                INNER JOIN hr_chapters ON hr_courses.id = hr_chapters.course_id
                INNER JOIN hr_lessons ON hr_lessons.chapter_id = hr_chapters.id
                INNER JOIN hr_user_lessons ON hr_user_lessons.lesson_id = hr_lessons.id
            WHERE
                hr_user_lessons.user_id = % s
                and hr_courses.id = % s;
        """
        chapters = list(Course.objects.raw(sql, (user_id.hex, course_id.replace('-', ''))))

        res_data = []
        for chapter in chapters:
            dict_lesson = dict(lesson_id=UUID(chapter.lesson_id))
            dict_lesson.update(lesson_title=chapter.lesson_title)
            dict_lesson.update(status=chapter.status)
            if len(res_data) == 0 or chapter.id != res_data[-1].get('chapter_id'):
                res_data.append({
                    'chapter_id': chapter.id,
                    'chapter_title': chapter.chapter_title,
                    'lessons': []
                })
            res_data[-1].get('lessons').append(dict_lesson)

        return res_data

    @classmethod
    def get_assigned_course(cls, user_id, params):
        assignment_queryset = Course.objects.filter(Q(assignments__user_id=user_id)).distinct()
        if params.get('course_name'):
            assignment_queryset = assignment_queryset.filter(title__icontains=params.get('course_name'))
        return assignment_queryset

    @classmethod
    def get_exclude_users_assignment(cls, course_id):
        return User.objects.exclude(Q(assignments__course_id = course_id))
