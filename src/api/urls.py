from api_base.views import ActionViewSet
from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

app_name = "api_base"
router = SimpleRouter(trailing_slash=False)

# Define url in here
router.register(r"actions", ActionViewSet, basename="actions")

urlpatterns = [
    url(r"^", include(router.urls)),
]
