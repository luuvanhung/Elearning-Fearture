from common.constants.wit_constants import WitEntities

from .base_parser import BaseParser


class CancelLeaveRequestParser(BaseParser):
    def __init__(self, wit_response):
        super().__init__(wit_response)

    def get_date_time(self):
        if self.entities.get(WitEntities.WIT_DATETIME):
            self.process_wit_datetime()
        elif self.entities.get(WitEntities.WIT_DURATION):
            self.process_wit_duration()
        else:
            self.intents_data_transfer_object["date_time"] = None
        return self
