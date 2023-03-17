# -*- coding: utf-8 -*-
from .provider import CustomKeycloakProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

urlpatterns = default_urlpatterns(CustomKeycloakProvider)
