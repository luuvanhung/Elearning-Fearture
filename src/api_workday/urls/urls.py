from api_workday.views.action_request import ActionRequestDetailViewSet
from api_workday.views.bonus_leave import BonusLeaveViewSet
from api_workday.views.bonus_type import BonusTypeViewSet
from api_workday.views.calendar import CalendarViewSet
from api_workday.views.date_off import DateOffViewSet
from api_workday.views.leave_type import LeaveTypeViewSet
from api_workday.views.leave_type_group import LeaveTypeGroupViewSet
from api_workday.views.remain_leave import RemainLeaveViewSet
from api_workday.views.request_off import RequestOffViewSet
from api_workday.views.statistic import StatisticDateOffView
from rest_framework.routers import SimpleRouter

app_name = "api_workday"

router = SimpleRouter(trailing_slash=False)
router.register(
    "admin/group-leave-types", LeaveTypeGroupViewSet, basename="group_leave_type"
)
router.register("admin/leave-types", LeaveTypeViewSet, basename="leave_type")
router.register("request-off", RequestOffViewSet, basename="request_off")
router.register("remain-leave", RemainLeaveViewSet, basename="remain_leave")
router.register(
    "request/management", ActionRequestDetailViewSet, basename="request_management"
)
router.register("date-off", DateOffViewSet, basename="date_off")
router.register("calendar", CalendarViewSet, basename="calendar")
router.register("statistic", StatisticDateOffView, basename="statistic")
router.register("bonus-leave", BonusLeaveViewSet, basename="bonus_leave")
router.register("bonus-type", BonusTypeViewSet, basename="bonus_type")
urlpatterns = router.urls
