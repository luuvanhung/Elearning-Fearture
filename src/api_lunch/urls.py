from api_lunch.views import LunchViewSet
from rest_framework.routers import SimpleRouter

app_name = "api_lunch"
router = SimpleRouter(trailing_slash=False)
router.register(r"", LunchViewSet, basename="lunches")
router_urlpatterns = router.urls
urlpatterns = router_urlpatterns
