from api_probation.models.evaluation_template_type import EvaluationTemplateType


def get_evaluation_template_type_by_name(type_name):
    return EvaluationTemplateType.objects.filter(type_name=type_name).first()
