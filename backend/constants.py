#!/usr/bin/env python
"""
File that contains the list of constants of the backend.
"""


class OAuth:
    """
    Contains Oauth2 constants.
    """
    PATH = '/o/token'
    ADMIN_WEBSIDE = '/admin'
    UNAUTHORIZED = 401


class Api:
    """
    Contains API constants.
    """
    PATH = '/api/v1'
    PROJECTS = '/qgisserver/project'
    PUBLISH = '/publish'
    DISABLE_PUBLICATION = '/disable'
    UNAUTHORIZED = 401


class Vault:
    """
    Contains the keyring constants.
    """
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"
