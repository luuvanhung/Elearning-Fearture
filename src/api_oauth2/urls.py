from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from .views import *

app_name = "api_oauth2"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"api_key", ApiViewSet, basename="api_key")
_urlpatterns = [
    path("login", csrf_exempt(login_view), name="login"),
    path("refresh_token", csrf_exempt(refresh_token_view), name="login"),
    path("logout", csrf_exempt(logout_view), name="logout"),
]
urlpatterns = router.urls + _urlpatterns
