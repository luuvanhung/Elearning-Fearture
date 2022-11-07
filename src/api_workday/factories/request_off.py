import factory
from api_workday.models import RequestOff
from faker import Factory

from .type_off import TypeOffFactory

faker = Factory.create()


class RequestOffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestOff

    reason = faker.word()
    type_off = factory.SubFactory(TypeOffFactory)
