from django.conf import settings

from common.constants.base_const import Const


class WitModules(Const):
    NAME = "Wit"
    BASE_URL = "https://api.wit.ai/"
    MESSAGE_API = "message?v=" + settings.WIT_API_VERSION + "&q="
    UTTERANCES_API = "utterances?v=" + settings.WIT_API_VERSION
