# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.socialaccount.providers.keycloak.provider import KeycloakProvider
from django.contrib.auth import get_user_model

OVERRIDE_NAME = (
    getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
    .get("customkeycloak", {})
    .get("OVERRIDE_NAME", "CustomKeycloak")
)


class CustomKeycloakProvider(KeycloakProvider):
    id = "customkeycloak"
    name = OVERRIDE_NAME
    settings = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get(
        "customkeycloak", {}
    )

    def _updateGroups(self, social_login, extra_data):
        if (groups := self.settings.get("GROUPS")) is not None and (
            mapping := groups.get("GROUP_TO_FLAG_MAPPING")
        ) is not None:
            filters = {
                social_login.user.USERNAME_FIELD: getattr(
                    social_login.user, social_login.user.USERNAME_FIELD
                )
            }
            user_model = get_user_model()
            try:
                user = user_model.objects.get(**filters)
                if user:
                    if isinstance(user, list) and len(user) > 0:
                        user = user[0]
                    # user = get_user_model().objects.get()
                    for flag, group in mapping.items():
                        if hasattr(user, flag):
                            if not isinstance(group, list):
                                group = [group]

                            value = any(
                                group_list_item in extra_data.get("groups", [])
                                for group_list_item in group
                            )

                            setattr(user, flag, value)
                            setattr(social_login.user, flag, value)
                    user.save()
            except user_model.DoesNotExist:
                print("User doesn't exist")
        pass

    def sociallogin_from_response(self, request, response):
        social_login = super().sociallogin_from_response(request, response)
        extra_data = self.extract_extra_data(response)
        self._updateGroups(social_login, extra_data)

        print(extra_data)
        return social_login


provider_classes = [CustomKeycloakProvider]
