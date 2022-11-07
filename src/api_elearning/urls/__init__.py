# from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter
from django.urls import path, include
from rest_framework_nested import routers

from ..views import ChapterViewSet, CourseViewSet, LessonViewSet, TopicViewSet, TranscriptViewSet, AttachmentViewSet, \
    AssignmentChapterViewSet, AssignmentViewSet, AssignmentChapterLessonViewSet, QuizViewSet, QuestionViewSet, \
    AssignmentChapterLessonAttachmentViewSet, QuizResultViewSet

app_name = "api_elearning"
# router = SimpleRouter(trailing_slash=False)
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'courses', CourseViewSet)
course_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
course_router.register(r'chapters', ChapterViewSet)

quiz_course_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
quiz_course_router.register(r'quizzes', QuizViewSet)

quiz_result_course_router = routers.NestedSimpleRouter(quiz_course_router, r'quizzes', lookup='quiz')
quiz_result_course_router.register(r'results', QuizResultViewSet)

question_course_router = routers.NestedSimpleRouter(quiz_course_router, r'quizzes', lookup='quiz')
question_course_router.register(r'questions', QuestionViewSet)

chapter_router = routers.NestedSimpleRouter(course_router, r'chapters', lookup='chapter')
chapter_router.register(r'lessons', LessonViewSet)

course_chapter_quiz_router = routers.NestedSimpleRouter(course_router, r'chapters', lookup='chapter')
course_chapter_quiz_router.register(r'quizzes', QuizViewSet)

question_course_chapter_quiz_router = routers.NestedSimpleRouter(course_chapter_quiz_router, r'quizzes', lookup='quiz')
question_course_chapter_quiz_router.register(r'questions', QuestionViewSet)

lesson_router = routers.NestedSimpleRouter(chapter_router, r'lessons', lookup='lesson')
lesson_router.register(r'attachments', AttachmentViewSet)

course_chapter_lesson_quiz_router = routers.NestedSimpleRouter(chapter_router, r'lessons', lookup='lesson')
course_chapter_lesson_quiz_router.register(r'quizzes', QuizViewSet)

question_course_chapter_lesson_quiz_router = routers.NestedSimpleRouter(course_chapter_lesson_quiz_router, r'quizzes',
                                                                        lookup='quiz')
question_course_chapter_lesson_quiz_router.register(r'questions', QuestionViewSet)

router.register(r'topics', TopicViewSet)
router.register(r'transcripts', TranscriptViewSet)

router.register(r'assignments', AssignmentViewSet)
assignment_router = routers.NestedSimpleRouter(router, r'assignments', lookup='assignment')
assignment_router.register(r'chapters', AssignmentChapterViewSet)

quiz_assignment_router = routers.NestedSimpleRouter(router, r'assignments', lookup='assignment')
quiz_assignment_router.register(r'quizzes', QuizViewSet)

quiz_assignment_result_router = routers.NestedSimpleRouter(quiz_assignment_router, r'quizzes', lookup='quiz')
quiz_assignment_result_router.register(r'results', QuizResultViewSet)

assignment_chapter_router = routers.NestedSimpleRouter(assignment_router, r'chapters', lookup='chapter')
assignment_chapter_router.register(r'lessons', AssignmentChapterLessonViewSet)

quiz_chapter_assignment_router = routers.NestedSimpleRouter(assignment_router, r'chapters', lookup='chapter')
quiz_chapter_assignment_router.register(r'quizzes', QuizViewSet)

quiz_chapter_result_assignment_router = routers.NestedSimpleRouter(quiz_chapter_assignment_router, r'quizzes',
                                                                   lookup='quiz')
quiz_chapter_result_assignment_router.register(r'results', QuizResultViewSet)

assignment_chapter_lesson_router = routers.NestedSimpleRouter(assignment_chapter_router, r'lessons',
                                                              lookup='lesson')

quiz_chapter_lesson_assignment_router = routers.NestedSimpleRouter(assignment_chapter_router, r'lessons',
                                                                   lookup='lesson')
quiz_chapter_lesson_assignment_router.register(r'quizzes', QuizViewSet)

quiz_chapter_lesson_result_assignment_router = routers.NestedSimpleRouter(quiz_chapter_lesson_assignment_router,
                                                                          r'quizzes', lookup='quiz')
quiz_chapter_lesson_result_assignment_router.register(r'results', QuizResultViewSet)

assignment_chapter_lesson_router.register(r'attachments', AssignmentChapterLessonAttachmentViewSet)

router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(course_router.urls)),
    path(r'', include(chapter_router.urls)),
    path(r'', include(lesson_router.urls)),
    path(r'', include(assignment_router.urls)),
    path(r'', include(assignment_chapter_router.urls)),
    path(r'', include(quiz_course_router.urls)),
    path(r'', include(question_course_router.urls)),
    path(r'', include(assignment_chapter_lesson_router.urls)),
    path(r'', include(quiz_result_course_router.urls)),
    path(r'', include(quiz_assignment_router.urls)),
    path(r'', include(quiz_assignment_result_router.urls)),
    path(r'', include(course_chapter_quiz_router.urls)),
    path(r'', include(question_course_chapter_quiz_router.urls)),
    path(r'', include(course_chapter_lesson_quiz_router.urls)),
    path(r'', include(question_course_chapter_lesson_quiz_router.urls)),
    path(r'', include(quiz_chapter_assignment_router.urls)),
    path(r'', include(quiz_chapter_result_assignment_router.urls)),
    path(r'', include(quiz_chapter_lesson_assignment_router.urls)),
    path(r'', include(quiz_chapter_lesson_result_assignment_router.urls)),
]
