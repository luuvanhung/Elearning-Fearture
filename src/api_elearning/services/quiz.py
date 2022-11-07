from api_base.services import BaseService
from api_elearning.models import Answer, Question, Quiz
from api_elearning.services import QuestionService


class QuizService(BaseService):
    @classmethod
    def create_multiple_questions(cls, quiz):
        quiz_questions = quiz.pop('quiz_questions')
        quiz = Quiz.objects.create(**quiz)
        order = 1
        question_arr = []
        question_answers_arr = []
        for question in quiz_questions:
            question.update({'quiz_id': quiz.id, 'order': order})
            question_answers = question.pop('question_answers')
            [answer.update({'order': order}) for answer in question_answers]
            [question_answers_arr.append(answer) for answer in question_answers]
            question_arr.append(Question(**question))
            order = order + 1

        question_created_arr = Question.objects.bulk_create(question_arr)
        answers_arr = []

        for answer in question_answers_arr:
            [answer.update({'question_id': question.id}) for question in question_created_arr
             if question.order == answer.get('order')]
            answers_arr.append(Answer(**answer))

        Answer.objects.bulk_create(answers_arr)
        return quiz

    @classmethod
    def update_question(cls, instance, quiz):
        quiz_questions = quiz.pop('quiz_questions')
        Quiz.objects.filter(pk=instance.id).update(**quiz)

        questions = []
        question_answers_arr = []
        question_ids = []
        answer_created = []

        for question in quiz_questions:
            if not question.get('id'):
                question.update({'quiz': instance, 'type_id': question.pop('type').get('id')})
                question_created = QuestionService.create_questions(question)
                question_ids.append(question_created.id)
                continue

            question_ids.append(question['id'])
            question_answers = question.pop('question_answers')
            question.update({'type_id': question.pop('type').get('id')})

            for answer in question_answers:
                if not answer.get('id'):
                    answer_created.append(Answer(**answer, question_id=question['id']))
                question_answers_arr.append(Answer(**answer))
            questions.append(Question(**question))

        Question.objects.filter(quiz_id=instance.id).exclude(id__in=question_ids).delete()
        Question.objects.bulk_update(questions, ['content', 'score', 'type_id', 'order'])
        Answer.objects.bulk_update(question_answers_arr, ['content', 'is_correct'])
        if answer_created:
            Answer.objects.bulk_create(answer_created)
        return Quiz(id=instance.id, **quiz)
