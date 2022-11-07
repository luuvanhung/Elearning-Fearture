from django.conf import settings
from django.db.models.functions import Lower

from api_base.services import BaseService
from api_elearning.constants import AssignmentStatus
from api_elearning.models import Assignment, AssignmentChapter, AssignmentChapterLessonAttachment
from api_elearning.models.assignment import AssignmentChapterLesson
from api_elearning.services.send_mail import SendEmailNotification
from api_elearning.services.send_notification_slack import SendSlackNotification
from django.db.models import Q


class AssignmentService(BaseService):
    @classmethod
    def create_assignment(cls, assignments, course_instance):
        course = course_instance.copy()
        created_assignments = []

        for assignment_item in assignments:
            assignment_existed = Assignment.objects.filter(
                Q(user=assignment_item.get('user')) & Q(
                    course=assignment_item.get('course')))
            if assignment_existed:
                assignment_obj = assignment_existed.first()
                if not assignment_obj.due_date:
                    raise Exception('Invalid start date or due date \'s assignment')

                assignment_existed = assignment_existed.filter(Q(
                    due_date__gte=assignment_item.get('start_date')) & Q(
                    start_date__gte=assignment_item.get('start_date')))
                if assignment_existed:
                    raise Exception('Invalid start date or due date \'s assignment')

            chapters = course.get('chapters')
            user = assignment_item.get('user')
            assignment = Assignment.objects.create(**assignment_item, full_name=user.profile.name,
                                                   course_name=course['title'])
            link = f"{settings.URL_WEB_INTERNAL}/my-assignments/{assignment.id}"
            assignment.link_to_course = link
            SendSlackNotification.send_notification_assignment(assignment=assignment)
            SendEmailNotification.send_new_assignment_notification(assignment=assignment)

            created_assignments.append(assignment)
            assignment_chapters = []
            assignment_lessons = []
            assignment_attachments = []
            for chapter in chapters:
                chapter_obj = {
                    "assignment_id": assignment.id,
                    "chapter_id": chapter['id'],
                    "chapter_name": chapter['title']
                }
                chapter_is_opened = False
                if not chapter['previous_chapter']:
                    chapter_obj.update({'status': AssignmentStatus.OPEN.value})
                    chapter_is_opened = True
                else:
                    chapter_obj.update(
                        {
                            'previous_assignment_chapter_id': chapter['previous_chapter'].get('id')
                        }
                    )
                assignment_chapter = AssignmentChapter(**chapter_obj)
                assignment_chapters.append(assignment_chapter)

                for lesson in chapter.get('lessons'):
                    lesson_obj = {
                        "assignment_chapter_id": str(assignment_chapter.id),
                        "lesson_id": lesson.get('id'),
                        "lesson_name": lesson.get('title')
                    }
                    if not lesson['previous_lesson']:
                        lesson_obj.update({'status': AssignmentStatus.OPEN.value})
                    else:
                        lesson_obj.update(
                            {
                                'previous_assignment_chapter_lesson_id': lesson['previous_lesson'].get('id')
                            }
                        )
                    assignment_lesson = AssignmentChapterLesson(**lesson_obj)
                    assignment_lessons.append(assignment_lesson)
                    for attachment in lesson.get('attachments'):
                        attachment_obj = {
                            "assignment_chapter_lesson_id": str(assignment_lesson.id),
                            "attachment_id": attachment.get('id'),
                            "read": False
                        }
                        assignment_attachment = AssignmentChapterLessonAttachment(**attachment_obj)
                        assignment_attachments.append(assignment_attachment)
            AssignmentChapter.objects.bulk_create(assignment_chapters)
            for assignment_chapter in assignment_chapters:
                if assignment_chapter.previous_assignment_chapter_id:
                    assignment_chapter.previous_assignment_chapter_id = [chapter for chapter in assignment_chapters
                                                                         if str(chapter.chapter_id) == str(
                            assignment_chapter.previous_assignment_chapter_id)][0].id
                    assignment_chapter.save()
            AssignmentChapterLesson.objects.bulk_create(assignment_lessons)
            for assignment_lesson in assignment_lessons:
                if assignment_lesson.previous_assignment_chapter_lesson_id:
                    assignment_lesson.previous_assignment_chapter_lesson_id = [lesson for lesson in assignment_lessons
                                                                               if str(lesson.lesson_id) == str(
                            assignment_lesson.previous_assignment_chapter_lesson_id)
                                                                               and str(
                            lesson.assignment_chapter_id) == str(assignment_lesson.assignment_chapter_id)][0].id
                    assignment_lesson.save()
            AssignmentChapterLessonAttachment.objects.bulk_create(assignment_attachments)
        return created_assignments

    @classmethod
    def get_all_assignments(cls, params):
        assignment_queryset = Assignment.objects.annotate(full_name_lower=Lower('full_name'),
                                                          course_title_lower=Lower('course__title')).filter()
        if params.get('keyword'):
            key = str(params.get('keyword')).strip().lower()
            assignment_queryset = assignment_queryset.filter(Q(full_name_lower__icontains=key) |
                                                             Q(course_title_lower__icontains=key))
        if params.get('statuses'):
            statuses = params['statuses'].split(',')
            assignment_queryset = assignment_queryset.filter(status__in=statuses)
        if params.get('from_date'):
            assignment_queryset = assignment_queryset.filter(Q(start_date__gte=params['from_date']))
        if params.get('to_date'):
            assignment_queryset = assignment_queryset.filter(Q(due_date__lte=params['to_date']) | Q(due_date=None))
        return assignment_queryset

    @classmethod
    def get_my_assignments(cls, user_id, params):
        assignment_queryset = Assignment.objects.filter(Q(user_id=user_id)).prefetch_related('course').order_by(
            '-created_at')
        assignments = []
        for assignment in assignment_queryset:
            if assignment.course and (len(assignments) == 0 or assignment.course.id != assignments[-1].id):
                assignment.course.assignment_id = str(assignment.id)
                assignment.course.assignment = None
                assignment.course.number_of_chapters = 0
                assignment.course.number_of_lessons = 0
                assignment.course.number_of_attachments = 0
                assignments.append(assignment.course)
        return assignments

    @classmethod
    def get_detail_assignment(cls, user_id, course_id):
        assignment_queryset = Assignment.objects.filter(Q(user_id=user_id) & Q(course_id=course_id))
        if not assignment_queryset.exists():
            raise Exception('Not found assignment')
        return assignment_queryset.first()

    @classmethod
    def get_users(cls, course_id, params):
        assignment_queryset = Assignment.objects.filter(Q(course_id=course_id))
        if params.get('full_name'):
            assignment_queryset = assignment_queryset.filter(full_name__icontains=params.get('full_name'))
        return assignment_queryset

    @classmethod
    def get_or_create_assignment(cls, assignment, course_instance):
        existed_assignment = Assignment.objects.filter(
            Q(course=course_instance['id']) & Q(user=assignment.get('user'))).last()
        if not existed_assignment:
            existed_assignment = AssignmentService.create_assignment([assignment], course_instance)[0]
        return existed_assignment
