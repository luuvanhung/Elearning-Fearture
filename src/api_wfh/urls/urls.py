from api_wfh.views.calendar import CalendarViewSet
from api_wfh.views.wfh_date import WfhDateViewSet
from api_wfh.views.wfh_request import WfhRequestViewSet
from rest_framework.routers import SimpleRouter

app_name = "api_wfh"

router = SimpleRouter(trailing_slash=False)
router.register("wfh-request", WfhRequestViewSet, basename="wfh_request")
router.register("wfh-date", WfhDateViewSet, basename="wfh_date")
router.register("calendar", CalendarViewSet, basename="calendar")
urlpatterns = router.urls
