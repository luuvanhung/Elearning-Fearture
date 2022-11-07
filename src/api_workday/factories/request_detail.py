import factory
from api_workday.models import RequestDetail
from faker import Factory

faker = Factory.create()


class RequestDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestDetail
