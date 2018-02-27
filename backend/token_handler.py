#!/usr/bin/env python
"""
Contains all the classes and constants required to request, refresh and handle
the server tokens.
"""

from urllib.parse import urljoin
import json

import requests
import keyring


class TokenHandler:
    """
    Acquires (requests to the server), saves (safely) and refreshes a token.
    """
    CLIENT_ID = ''  # TODO: add client ID

    GISCUBE_OAUTH_PATH = 'o/token/'
    GISCUBE_OAUTH_BAD_CREDENTIALS_STATUS = 401

    KEYRING_APP_NAME = "giscube-admin-qgis-plugin"
    KEYRING_TOKEN_KEY = "access_token"
    KEYRING_REFRESH_TOKEN_KEY = "refresh_token"

    def __init__(self, server_url):
        """
        Contructor. Loads the saved tokens.
        """
        self.__loadTokens()
        self._server_url = server_url

    @property
    def server_url(self):
        """
        Gets the URL of the credentials of the server.
        """
        return self._server_url

    @property
    def token(self):
        """
        Get the current token.
        """
        return self.__token

    def hasToken(self):
        """
        Does it have a token?
        """
        return self.__token is not None

    def hasRefreshToken(self):
        """
        Does it have a refresh token?
        """
        return self.__refreshToken is not None

    def refreshToken(self):
        """
        Refreshes the token with the refresh token. Returns if it succeded.
        """
        if not self.hasRefreshToken():
            return False

        response = requests.post(
            urljoin(self._server_url, self.GISCUBE_OAUTH_PATH),
            data={
                'refresh-token': self.refresh_token,
                'grant_type': 'refresh_token',
                'client_id': self.CLIENT_ID,
            }
        )

        if response == self.GISCUBE_OAUTH_BAD_CREDENTIALS_STATUS:
            return False

        response.raise_for_status()
        response_object = json.load(response.content)

        token = response_object['access_token']
        refreshToken = response_object['refresh_token']

        self.__token = token
        self.__refreshToken = refreshToken
        self.__saveTokens()

        return True

    def requestNewToken(self, user, password):
        """
        Requests a new token to the server. Returns if succeded.
        It will raise a requests.exceptions.HTTPError if the server responses
        with an error status code.
        """

        response = requests.post(
            urljoin(self._server_url, self.GISCUBE_OAUTH_PATH),
            data={
                'user': user,
                'password': password,
                'grant_type': 'password',
                'client_id': self.CLIENT_ID,
            }
        )

        if response == self.GISCUBE_OAUTH_BAD_CREDENTIALS_STATUS:
            return False
        response.raise_for_status()
        response_object = json.load(response.content)

        if 'access_token' in response_object:
            token = response_object['access_token']
        else:
            return False

        refreshToken = None
        if 'refresh-token' in response_object:
            refreshToken = response_object['refresh-token']

        self.__token = token
        self.__refreshToken = refreshToken
        self.__saveTokens()

        return True

    def __loadTokens(self):
        """
        Loads the tokens in a safe place.
        """
        self.token = keyring.get_password(
            self.KEYRING_APP_NAME,
            self.KEYRING_TOKEN_KEY)
        self.refresh_token = keyring.get_password(
            self.KEYRING_APP_NAME,
            self.KEYRING_REFRESH_TOKEN_KEY)

    def __saveTokens(self):
        """
        Saves the tokens in a safe place.
        """
        keyring.delete_password(
            self.KEYRING_APP_NAME,
            self.KEYRING_TOKEN_KEY)
        keyring.delete_password(
            self.KEYRING_APP_NAME,
            self.KEYRING_REFRESH_TOKEN_KEY)

        if self.token is not None:
            keyring.set_password(
                self.KEYRING_APP_NAME,
                self.KEYRING_TOKEN_KEY,
                self.token)
        if self.refresh_token is not None:
            keyring.set_password(
                self.KEYRING_APP_NAME,
                self.KEYRING_REFRESH_TOKEN_KEY,
                self.refresh_token)
