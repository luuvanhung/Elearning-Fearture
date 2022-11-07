from rest_framework import routers

from .views import TeamViewSet

app_name = "api_team"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", TeamViewSet, basename="team")

urlpatterns = router.urls
