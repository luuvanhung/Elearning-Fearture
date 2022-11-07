from core.settings.base import DEFAULT_CLIENT_ID, DEFAULT_CLIENT_SECRET


class ClientGenerator:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        post_dict = request.POST.copy()
        if (
            post_dict.get("client_id") == "undefined"
            or post_dict.get("client_id") is None
        ):
            post_dict["client_id"] = DEFAULT_CLIENT_ID
            post_dict["client_secret"] = DEFAULT_CLIENT_SECRET
        else:
            post_dict["client_id"] = post_dict.get("client_id", DEFAULT_CLIENT_ID)
            post_dict["client_secret"] = post_dict.get(
                "client_secret", DEFAULT_CLIENT_SECRET
            )
        request.POST = post_dict
