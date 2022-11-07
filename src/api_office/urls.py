from api_office.views import DepartmentViewSet, GroupViewSet, HolidayViewSet, OfficeViewSet, SquadViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

app_name = "api_office"
router = SimpleRouter(trailing_slash=False)
router.register(r"group", GroupViewSet, basename="group")
router.register(r"department", DepartmentViewSet, basename="department")
router.register(r"squad", SquadViewSet, basename="squad")
office = router.register(r"", OfficeViewSet, basename="office")
office.register(
    r"holidays", HolidayViewSet, basename="holiday", parents_query_lookups="office"
)

urlpatterns = router.urls
