from common.constants.wit_constants import WitEntities
from common.constants.workday_constants import Leave

from .base_parser import BaseParser


class CreateLeaveRequestParser(BaseParser):
    def __init__(self, wit_response):
        super().__init__(wit_response)

    def get_user_reason(self):
        if WitEntities.REASON in self.entities:
            self.intents_data_transfer_object["reason"] = self.entities[
                WitEntities.REASON
            ][0].get("value")
        else:
            self.intents_data_transfer_object["reason"] = Leave.DEFAULT_LEAVE_REASON
        return self
