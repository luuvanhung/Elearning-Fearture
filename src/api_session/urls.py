from api_session.views import SessionViewSet
from rest_framework import routers

app_name = "api_session"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", SessionViewSet, basename="session")

urlpatterns = router.urls
