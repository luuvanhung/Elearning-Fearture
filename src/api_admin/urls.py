from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from .views import AdminViewSet

app_name = "api_admin"
router = SimpleRouter(trailing_slash=False)

router.register(r"", AdminViewSet, basename="admins")


urlpatterns = [
    url(r"^", include(router.urls)),
]
