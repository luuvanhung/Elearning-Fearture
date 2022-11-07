from django.urls import path, include
from rest_framework_nested import routers
from ..views import AttachmentViewSet

attachment_router = routers.SimpleRouter(trailing_slash=False)
attachment_router.register(r'', AttachmentViewSet)
urlpatterns = [ path(r'', include(attachment_router.urls)), ]