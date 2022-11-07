import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import get_resolver


class Command(BaseCommand):
    help = "Create permissions with url pattern"

    @property
    def get_registries(self) -> list:
        """
        Return all registry of router is registered in url pattern
        """
        patterns = get_resolver().url_patterns
        api_patterns = [
            pattern
            for pattern in patterns
            if (
                hasattr(pattern, "app_name")
                and getattr(pattern, "app_name") in settings.LOCAL_APPS
            )
        ]
        registries: list = list()
        for pattern in api_patterns:
            urlconf_name = getattr(pattern, "urlconf_name")
            if hasattr(urlconf_name, "router"):
                registries.append(getattr(urlconf_name, "router").registry)
        return registries

    @property
    def get_api_actions(self) -> set:
        from api_oauth2.permissions import Oauth2Permissions
        from rest_framework.routers import SimpleRouter

        registries: list = self.get_registries
        api_actions = []
        for registry in registries:
            for res in registry:
                res_dict = {res[1].__name__: res[2]}
                if Oauth2Permissions in res[1].permission_classes:
                    router = SimpleRouter()
                    routes = router.get_routes(res[1])
                    action_list = []
                    for route in routes:
                        action_list += list(route.mapping.values())
                    distinct_action_list = set(action_list)
                    if "partial_update" in distinct_action_list:
                        distinct_action_list.remove("partial_update")
                    basename = res_dict.get(res[1].__name__)
                    api_actions.extend(
                        [f"{basename}:{action}" for action in distinct_action_list]
                    )
        api_actions = set(api_actions)
        return api_actions

    def handle(self, *args, **kwargs):
        try:
            data = dict()
            for scope in self.get_api_actions:
                """
                Create description of scope
                """
                name_scope = scope.split(":")
                basename = name_scope[0].replace("_", " ")  # name of scope: album
                action_name = name_scope[1].replace("_", " ")  # name of action: create
                description = f"{action_name.title()} object of {basename.title()}"

                data.update({scope: description})
            json_path = settings.SCOPES_JSON_PATH
            with open(json_path, "w+", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            if os.path.exists(json_path):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[+] SUCCESS: Create successfully {len(data)} scopes"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[X] FAILED: {e}"))
