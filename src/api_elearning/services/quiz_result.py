from api_base.services import BaseService
from api_elearning.models import QuizResult, QuizResultDetail, QuizResultDetailAnswer


class QuizResultService(BaseService):
    @classmethod
    def create_quiz_result(cls, quiz_result, quiz):
        obj_result = dict({
            'quiz': quiz_result['quiz'],
            'user': quiz_result['user'],
            'assignment_chapter': quiz_result['assignment_chapter']
        })
        existed_quiz_result = QuizResult.objects.filter(**obj_result)
        if existed_quiz_result.exists():
            passed_quiz_result = existed_quiz_result.first().is_passed
            if passed_quiz_result:
                raise Exception('Only do this quiz once!')
            else:
                existed_quiz_result.delete()

        quiz_result_details = quiz_result.pop('quiz_result_details')
        created_quiz_result = QuizResult(**quiz_result)

        questions = []
        answers = []
        for question in quiz_result_details:
            detail_answers = question.pop('quiz_result_detail_answers')
            question.update({'quiz_result': created_quiz_result})
            detail_question_obj = QuizResultDetail(**question)
            score = question['question'].score
            correct_answer = True

            for answer in detail_answers:
                if answer['answer'].is_correct != answer['chosen']:
                    correct_answer = False
                    score = 0
                else:
                    correct_answer = True
                answer.update({'quiz_result_detail': detail_question_obj, 'correct': correct_answer})
                answers.append(QuizResultDetailAnswer(**answer))

            detail_question_obj.score = score
            questions.append(detail_question_obj)

        score_user = 0
        score_quiz = 0
        for q in questions:
            score_user = score_user + q.score
            score_quiz = score_quiz + q.question.score

        created_quiz_result.threshold = score_user / score_quiz
        if created_quiz_result.threshold >= created_quiz_result.quiz.threshold:
            created_quiz_result.is_passed = True
        created_quiz_result.save()

        QuizResultDetail.objects.bulk_create(questions)
        QuizResultDetailAnswer.objects.bulk_create(answers)

        return created_quiz_result
