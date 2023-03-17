# -*- coding: utf-8 -*-
from django.test.utils import override_settings

from allauth.socialaccount.tests import OpenIDConnectTests
from allauth.tests import MockedResponse, TestCase

from .provider import CustomKeycloakProvider


@override_settings(
    SOCIALACCOUNT_PROVIDERS={
        CustomKeycloakProvider.id: dict(
            KEYCLOAK_URL="https://keycloak.unittest.example",
            KEYCLOAK_REALM="unittest",
        )
    }
)
class KeycloakTests(OpenIDConnectTests, TestCase):
    provider_id = CustomKeycloakProvider.id

    def get_mocked_response(self):
        return MockedResponse(
            200,
            """
            {
                "picture": "https://secure.gravatar.com/avatar/123",
                "email": "mr.bob@your.Keycloak.server.example.com",
                "id": 2,
                "sub": 2,
                "identities": [],
                "name": "Mr Bob"
            }
        """,
        )
