from api_seat_map.views import ObjectTypeViewSet, ObjectViewSet
from rest_framework import routers

app_name = "api_seat_map"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"object-type", ObjectTypeViewSet, basename="object_type")
router.register(r"object", ObjectViewSet, basename="object")

urlpatterns = router.urls
