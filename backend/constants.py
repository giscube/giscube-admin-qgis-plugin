#!/usr/bin/env python
"""
File that contains the list of constants of the backend.
"""


class Oauth:
    """
    Contains Oauth2 constants.
    """
    PATH = 'o/token/'
    BAD_CREDENTIALS_STATUS = 401


class Api:
    """
    Contains API constants.
    """
    PATH = 'api/v1/'
    PROJECTS = 'projects/'
    BAD_CREDENTIALS = 401


class Vault:
    """
    Contains the keyring constants.
    """
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"
