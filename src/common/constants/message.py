from typing import List

from common.constants.base_const import Const

__all__ = ["ResponseMessages"]


class ResponseMessages(Const):
    CREATED = "Created {0} Successfully"
    UPDATED = "Updated {0} Successfully"
    DELETED = "Deleted {0} Successfully"

    @classmethod
    def get_response_message(cls, message: str, params: List[str] = []) -> str:
        return message.format(*params)
