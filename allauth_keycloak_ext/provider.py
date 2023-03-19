# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.socialaccount.providers.keycloak.provider import KeycloakProvider
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

OVERRIDE_NAME = (
    getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
    .get("keycloak_ext", {})
    .get("OVERRIDE_NAME", "Keycloak Ext")
)


class KeycloakExtProvider(KeycloakProvider):
    id = "keycloak_ext"
    name = OVERRIDE_NAME
    settings = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get(
        "keycloak_ext", {}
    )

    def _autoCreateGroups(self, user, groups, groups_mapping):
        for group_name in groups:
            if group_name not in groups_mapping:
                self._add_user_to_group(user, group_name)

    def _add_user_to_group(self, user, group_name):
        # Check if group exists
        group, created = Group.objects.get_or_create(name=group_name)

        # If the group was just created, add the user to the group
        if created:
            group.user_set.add(user)

        # If the group already exists, check if the user is not already in the group
        elif user not in group.user_set.all():
            group.user_set.add(user)

    def _mapGroups(self, user, groups, groups_mapping):
        for keycloakGroup, djangoGroup in groups_mapping.items():
            if keycloakGroup in groups and djangoGroup and len(djangoGroup) > 1:
                self._add_user_to_group(user, djangoGroup)

    def _updateFlags(self, social_login, user, extra_data, mapping):
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

    def _updateGroups(self, social_login, extra_data):
        if (groups_settings := self.settings.get("GROUPS")) is not None:
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

                    if groups_settings.get("GROUPS_AUTO_CREATE"):
                        groups = extra_data.get("groups", [])
                        self._autoCreateGroups(
                            user, groups, groups_settings.get("GROUPS_MAPPING")
                        )

                    if (
                        groups_mapping := groups_settings.get("GROUPS_MAPPING")
                    ) is not None:
                        groups = extra_data.get("groups", [])
                        self._mapGroups(user, groups, groups_mapping)

                    if (
                        flags_mapping := groups_settings.get(
                            "GROUP_TO_FLAG_MAPPING"
                        )
                    ) is not None:
                        self._updateFlags(
                            social_login, user, extra_data, flags_mapping
                        )

                    user.save()
            except user_model.DoesNotExist:
                print("User doesn't exist")

    def sociallogin_from_response(self, request, response):
        social_login = super().sociallogin_from_response(request, response)
        extra_data = self.extract_extra_data(response)
        self._updateGroups(social_login, extra_data)

        print(extra_data)
        return social_login


provider_classes = [KeycloakExtProvider]
