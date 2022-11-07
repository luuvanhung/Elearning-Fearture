import logging

from api_user.models import User
from api_user.tests.factories import UserFactory
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .factories import ApplicationFactory
from .factories.oauth2_auth import OauthClient
from .models import Application
from .serializers import ApplicationSerializer

LOG = logging.getLogger(__name__)


class ApplicationTestCase(APITestCase):
    def setUp(self):
        self.rq_factory = APIRequestFactory()
        self.user = UserFactory.create()
        self.application = ApplicationFactory.create(
            user=self.user, name=self.user.email
        )
        self.client_class = OauthClient(enforce_csrf_checks=True)

    def test_authenticate(self):
        access_token = self.client_class.authenticate(
            user=self.user, application=self.application
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get("/api/v1/dates")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Expected response code 200 but got {response.status_code} instead",
        )

    def test_create_application(self):
        application = ApplicationFactory.create()
        APITestCase.assertIsInstance(self, application, Application)

    def test_get_list_applications(self):
        user = User.objects.get(pk=self.user.id)
        self.client.force_authenticate(
            user=user,
        )
        response = self.client.get("/api/v1/oauth2/applications")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Expected response code 200 but got {response.status_code} instead",
        )

        applications = Application.objects.filter(user=self.user)
        application_serializer = ApplicationSerializer(applications, many=True)
        self.assertListEqual(
            response.data,
            application_serializer.data,
            msg="Returned list not matched",
        )
