from api_base.services import BaseService
from api_elearning.models import Answer, Question
from django.db.models import Q


class QuestionService(BaseService):
    @classmethod
    def create_questions(cls, question):
        answers = question.pop('question_answers')
        order = question['order']
        question_updates = Question.objects.filter(Q(quiz_id=question['quiz'].id) & Q(order__gte=order)).values('pk',
                                                                                                                'order')

        questions = []
        if question_updates.exists():
            for question_update in question_updates:
                order = order + 1
                question_update['order'] = order
                questions.append(Question(**question_update))

        question = Question.objects.create(**question)
        Question.objects.bulk_update(questions, ['order'])

        ans = [Answer(**ans, question_id=question.id) for ans in answers]
        Answer.objects.bulk_create(ans)
        return question

    @classmethod
    def update_questions(cls, instance, question_obj):
        answers = question_obj.pop('question_answers')
        Question.objects.filter(Q(pk=instance.id)).update(**question_obj)
        ans = [Answer(**ans) for ans in answers]
        Answer.objects.bulk_update(ans, ["content"])
        return question_obj
