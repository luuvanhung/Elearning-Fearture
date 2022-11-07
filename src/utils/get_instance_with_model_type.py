from django.contrib.contenttypes.models import ContentType


def get_instance_with_model_type(instance_id, model_type: ContentType):
    """
    Get instance by id and model type from ContentType
    """
    query_instance = model_type.get_object_for_this_type(id=instance_id)
    return query_instance
