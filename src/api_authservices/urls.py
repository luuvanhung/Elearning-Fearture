from api_authservices.views import GoogleLoginApi
from django.urls import include, path

login_patterns = [
    path("google/", GoogleLoginApi.as_view(), name="login-with-google"),
]

urlpatterns = [path("login/", include(login_patterns))]
