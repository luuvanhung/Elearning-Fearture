from api_base.services import BaseService
from api_oauth2.models import Application


class ApplicationService(BaseService):
    @classmethod
    def get_list(cls, request):
        return Application.objects.all().order_by("created")
