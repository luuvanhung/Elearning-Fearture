from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from health_check.urls import urlpatterns as health_check_urls
from rest_framework import permissions

from .views import embed_view, privacy_policy_view, single_page_view, terms_of_use_view

schema_view = get_schema_view(
    openapi.Info(
        title="PARADOX ERP API",
        default_version="v1",
        description="Paradox ERP api documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="damelagi@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path("api/v1/", include("api.urls")),
        path("api/v1/o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
        path("api/v1/admins/", include("api_admin.urls")),
        path("api/v1/lunches/", include("api_lunch.urls")),
        path("api/v1/workday/", include("api_workday.urls")),
        path("api/v1/wfh/", include("api_wfh.urls")),
        path("api/v1/user/", include("api_user.urls")),
        path("api/v1/provider/", include("api_providers.urls")),
        path("api/v1/probation/", include("api_probation.urls")),
        path("api/v1/user-lunch/", include("api_user_lunch.urls")),
        path("api/v1/event/", include("api_event.urls")),
        path("api/v1/team/", include("api_team.urls")),
        path("api/v1/oauth2/", include("api_oauth2.urls")),
        path("api/v1/authenservice/", include("api_authservices.urls")),
        path("api/v1/skill/", include("api_skill.urls")),
        path("api/v1/office/", include("api_office.urls")),
        path("api/v1/session/", include("api_session.urls")),
        path("api/v1/seat-map/", include("api_seat_map.urls")),
        path("api/v1/slack-bot/", include("api_slackbot.urls")),
    ],
)

urlpatterns = [
    url(r"^embed/", embed_view),
    url(r"^api/v1/embed/attachments/", include("api_elearning.urls.embed_urls")),
    url(r"^healthcheck/", include(health_check_urls)),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r"^api/v1/", include(("api.urls", "api"), namespace="v1")),
    url(r"^api/v1/o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    url(r"^api/v1/admins/", include("api_admin.urls")),
    url(r"^api/v1/workday/", include("api_workday.urls.urls")),
    url(r"^api/v1/wfh/", include("api_wfh.urls")),
    url(r"^api/v1/user/", include("api_user.urls")),
    url(r"^api/v1/provider/", include("api_providers.urls")),
    url(r"^api/v1/probation/", include("api_probation.urls")),
    url(r"^api/v1/lunches/", include("api_lunch.urls")),
    url(r"^api/v1/user-lunch/", include("api_user_lunch.urls")),
    url(r"^api/v1/event/", include("api_event.urls")),
    url(r"^api/v1/team/", include("api_team.urls")),
    url(r"^api/v1/oauth2/", include("api_oauth2.urls")),
    url(r"api/v1/skill/", include("api_skill.urls")),
    url(r"api/v1/office/", include("api_office.urls")),
    url(r"api/v1/session/", include("api_session.urls")),
    url("api/v1/seat-map/", include("api_seat_map.urls")),
    url("api/v1/slack-bot/", include("api_slackbot.urls")),
    url("api/v1/elearning/", include("api_elearning.urls")),
    url("api/v1/authenservice/", include("api_authservices.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# File url
urlpatterns += [
    url(r"^api/v1/", include("binary_database_files.urls")),  # path api/v1/files/
]
if settings.ALLOWED_SWAGGER:
    # Swagger
    urlpatterns += [
        path(
            "api/v1/swagger.json",
            schema_view.without_ui(cache_timeout=0),
            name="erp_schema-json",
        ),
        path(
            "api/v1/swagger",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="erp-schema-swagger-ui",
        ),
    ]

# Root route
urlpatterns += [
    url(r"^terms-of-use/", terms_of_use_view),
    url(r"^privacy-policy/", privacy_policy_view),
    url(r"^.*$", single_page_view),
]
