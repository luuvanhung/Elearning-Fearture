from api_base.services.base import BaseService
from django.conf import settings
from slack_sdk import WebClient


class SlackBaseService(BaseService):
    def __init__(self):
        self.client = WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)
