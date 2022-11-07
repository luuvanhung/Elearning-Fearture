from django.urls import path

from .views import SlackInteractiveComponentsHandler, SlackMessageHandler

urlpatterns = [
    path("slack/events", SlackMessageHandler.as_view(), name="slack_events"),
    path(
        "slack/actions",
        SlackInteractiveComponentsHandler.as_view(),
        name="slack_events",
    ),
]
