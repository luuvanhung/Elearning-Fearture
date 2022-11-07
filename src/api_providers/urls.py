from api_providers.views import HandleProvider
from rest_framework.routers import SimpleRouter

app_name = "api_providers"

router = SimpleRouter(trailing_slash=False)
router.register("", HandleProvider, basename="provider")
router_urlpatterns = router.urls
urlpatterns = router_urlpatterns
