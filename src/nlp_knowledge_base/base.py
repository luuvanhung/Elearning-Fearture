from common.constants.wit_constants import WitModules

from .services.wit.service import WitService


class NlpService:
    _engine_name = None
    _engine = None
    _access_token = None
    returned_intents = None

    def __init__(self, engine_name, access_token):
        self._engine_name = engine_name
        self._access_token = access_token

    def get_engine(self):
        if self._engine_name == WitModules.NAME:
            self._engine = WitService(self._access_token)
        return self

    def get_intents(self, message):
        self.returned_intents = self._engine.get_intents(message)
        return self
