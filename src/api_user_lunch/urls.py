from django.urls import include, path
from rest_framework import routers

from . import views
from .views import AdminViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("", AdminViewSet)

app_name = "api_user_lunch"
urlpatterns = [
    path("", views.HandleUserLunch.as_view(), name="get-user-lunches"),
    path("get-paginate", views.GetUserLunches.as_view()),
    path("create", views.HandleUserLunch.as_view(), name="create-user-lunch"),
    path(
        "create-many",
        views.HandleManyUserLunch.as_view(),
        name="create-many-user-lunch",
    ),
    path(
        "delete-many",
        views.HandleManyUserLunch.as_view(),
        name="delete-many-user-lunch",
    ),
    path(
        "admin-create",
        views.HandleUserLunchByAdmin.as_view(),
        name="admin-create-user-lunch",
    ),
    path(
        "admin-update/<uuid:pk>",
        views.HandleUserLunchByAdmin.as_view(),
        name="admin-update-user-lunch",
    ),
    path("action/<uuid:pk>", views.HandleUserLunch.as_view(), name="modify-user-lunch"),
    path("all", views.GetAllUserLunches.as_view()),
    path("set-veggie", views.SetVeggieUserLunch.as_view(), name="set-veggie-lunch"),
    path(
        "cancel-veggie",
        views.CancelSetVeggieUserLunch.as_view(),
        name="cancel-veggie-lunch",
    ),
    path("", include(router.urls)),
]
