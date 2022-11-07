from common.constants.base_const import Const

__all__ = ["HttpMethod"]


class HttpMethod(Const):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    HEAD = "head"
    OPTIONS = "options"
    PATCH = "patch"
