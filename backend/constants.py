#!/usr/bin/env python
"""
File that contains the list of constants of the backend.
"""


class OAuth:
    """
    Contains Oauth2 constants.
    """
    PATH = 'o/token/'
    UNAUTHORIZED = 401


class Api:
    """
    Contains API constants.
    """
    PATH = 'api/v1/'
    PROJECTS = 'qgisserver/project/'
    UNAUTHORIZED = 401


class Vault:
    """
    Contains the keyring constants.
    """
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"
