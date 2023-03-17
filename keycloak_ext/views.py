# -*- coding: utf-8 -*-

from allauth.socialaccount.providers.keycloak.views import (
    KeycloakOAuth2Adapter
)
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import CustomKeycloakProvider


class CustomKeycloakOAuth2Adapter(KeycloakOAuth2Adapter):
    provider_id = CustomKeycloakProvider.id


oauth2_login = OAuth2LoginView.adapter_view(CustomKeycloakOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomKeycloakOAuth2Adapter)
