import requests
from common.constants.api_constants import HttpMethod
from common.constants.wit_constants.modules import WitModules


def request_header_generator(access_token, auth_type="Bearer"):
    return {"Authorization": auth_type + " " + access_token}


def req(path, access_token, method, params="", body=None):
    if body is None:
        body = {}

    full_url = WitModules.BASE_URL + path + params
    request_header = request_header_generator(access_token)

    if method == HttpMethod.GET:
        rsp = requests.get(url=full_url, headers=request_header)
        return rsp.json()
    if method == HttpMethod.POST:
        rsp = requests.post(url=full_url, headers=request_header, data=body)
        return rsp.json()


class WitService:
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token

    def get_intents(self, message):
        rsp = req(
            path=WitModules.MESSAGE_API,
            access_token=self.access_token,
            method=HttpMethod.GET,
            params=self.message_transfer_params(message),
        )
        return rsp

    @staticmethod
    def message_transfer_params(message):
        return message.replace(" ", "%20")
