import logging
import typing

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from rest_framework_api_key.permissions import BaseHasAPIKey

from ..models import ApiKey

log = logging.getLogger("oauth2_provider")


class HasOauth2ApiKey(BaseHasAPIKey):
    model = ApiKey

    def get_required_alternate_scopes(self, request, view):
        try:
            return getattr(view, "required_alternate_scopes")
        except AttributeError:
            raise ImproperlyConfigured(
                "TokenHasActionScope requires the view to"
                " define the required_alternate_scopes attribute"
            )

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        assert self.model is not None, (
            "%s must define `.model` with the API key model to use"
            % self.__class__.__name__
        )
        key = self.get_key(request)
        if not key:
            return False
        required_alternate_scopes = self.get_required_alternate_scopes(request, view)
        action = view.action.lower()
        api_key = self.model.objects.get_api_key(key)
        if api_key is not None:
            if action in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {}".format(
                        required_alternate_scopes[action]
                    )
                )
                return any(
                    api_key.has_scopes(alt) for alt in required_alternate_scopes[action]
                )
            else:
                log.warning(f"no scope alternates defined for method {action}")
                return True

        return False
