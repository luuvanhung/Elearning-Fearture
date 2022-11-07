import logging

from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

log = logging.getLogger("oauth2_provider")


class IsOwnerOrHasScope(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    using in personal information user (bank, contact, education, family, identity, insurance)
    """

    def get_required_alternate_scopes(self, request, view):
        try:
            return getattr(view, "required_alternate_scopes")
        except AttributeError:
            raise ImproperlyConfigured(
                "TokenHasActionScope requires the view to"
                " define the required_alternate_scopes attribute"
            )

    def has_object_permission(self, request, view, obj):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):  # OAuth 2
            required_alternate_scopes = self.get_required_alternate_scopes(
                request, view
            )
            action = view.action.lower()
            if action in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {}".format(
                        required_alternate_scopes[action]
                    )
                )
                result = any(
                    token.is_valid(alt) for alt in required_alternate_scopes[action]
                )
                if result:
                    return True
                else:
                    allowed_object_permission_action = [
                        "update",
                        "retrieve",
                        "partial_update",
                        "create",
                        "add",
                        "destroy",
                    ]
                    if view.action not in allowed_object_permission_action:
                        return False
                    if view.action == "add" or view.action == "retrieve":
                        return True if obj == request.user else False
                    else:
                        return obj.user == request.user
            else:
                log.warning(f"no scope alternates defined for method {action}")
                return True
