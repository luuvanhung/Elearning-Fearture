import factory
from api_user.tests.factories import UserFactory
from common.constants.api_oauth2 import ApplicationChoice
from faker import Faker

from ..models import Application
from ..utils import convert_list_to_space_separated

fake = Faker()
scopes = [
    "application:list",
    "application:create",
    "application:retrieve",
    "application:update",
    "application:destroy",
    "wrong:scopes",
    "application",
]
application_scopes = convert_list_to_space_separated(scopes)


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application
        django_get_or_create = ("user",)

    redirect_uris = fake.uri()
    user = factory.SubFactory(UserFactory)
    algorithm = factory.Iterator(ApplicationChoice.ALGORITHM_TYPES)
    authorization_grant_type = ApplicationChoice.GRANT_PASSWORD
    client_type = ApplicationChoice.CLIENT_CONFIDENTIAL
    scope = application_scopes
