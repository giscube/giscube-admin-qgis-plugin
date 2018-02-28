#!/usr/bin/env python
"""
Contains all the classes and constants required to request, refresh and handle
the server tokens.
"""

import json

import requests
import keyring

from .utils import urljoin


class TokenHandler:
    """
    Acquires (requests to the server), saves (safely) and refreshes a token.
    """

    GISCUBE_OAUTH_PATH = 'o/token'
    GISCUBE_OAUTH_BAD_CREDENTIALS_STATUS = 401

    KEYRING_APP_NAME = "giscube-admin-qgis-plugin"
    KEYRING_TOKEN_KEY = "access_token"
    KEYRING_REFRESH_TOKEN_KEY = "refresh_token"

    def __init__(
            self,
            server_url,
            client_id,
            save_tokens=True,
            keyring_name=None):
        """
        Contructor. Loads, if enabled, the saved tokens.
        :param server_url: Used server service URL
        :type server_url: str
        :param client_id: Application Oauth client ID
        :type client_id: str or unicode
        :param save_tokens: Enables saving the tokens locally (using the OS
        "safe" system)
        :type save_tokens: bool
        """

        self._server_url = server_url
        self._client_id = client_id

        self._save = save_tokens
        if keyring_name is not None:
            self._keyring_client_name = keyring_name
        else:
            self._keyring_client_name = self.KEYRING_APP_NAME

        self.__loadTokens()

    @property
    def server_url(self):
        """
        Gets the URL of the credentials of the server.
        """
        return self._server_url

    @property
    def client_id(self):
        """
        Gets the client ID for this server.
        """
        return self._client_id

    @property
    def has_access_token(self):
        """
        Does it have an access token?
        """
        return self.__access_token is not None

    @property
    def access_token(self):
        """
        Get the current access token.
        """
        return self.__access_token

    @property
    def has_refresh_token(self):
        """
        Does it have a refresh token?
        """
        return self.__refresh_token is not None

    def login(self, user, password):
        """
        Requests a new token to the server. Returns if succeded.
        :param user: User's username
        :type user: str or unicode
        :param password: User's password
        :type password: str or unicode
        :raises requests.exceptions.HTTPError: when the server responses with
        an unexpected error status code
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
            self.__access_token = response_object['access_token']
        else:
            return False

        self.__refresh_token = None
        if 'refresh-token' in response_object:
            self.__refresh_token = response_object['refresh-token']

        self.__save_tokens()

        return True

    def refresh_token(self):
        """
        Refreshes the token with the refresh token. Returns if it succeded.
        """
        if not self.has_refresh_token:
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
        refresh_token = response_object['refresh_token']

        self.__token = token
        self.__refresh_token = refresh_token
        self.__saveTokens()

        return True

    def __load_tokens(self):
        """
        Loads the tokens in a safe place.
        """
        if not self._save:
            return

        self.__access_token = keyring.get_password(
            self._keyring_client_name,
            self.KEYRING_TOKEN_KEY)
        self.__refresh_token = keyring.get_password(
            self.KEYRING_APP_NAME,
            self.KEYRING_REFRESH_TOKEN_KEY)

    def __save_tokens(self):
        """
        Saves the tokens in a safe place.
        """
        if not self._save:
            return

        keyring.delete_password(
            self._keyring_client_name,
            self.KEYRING_TOKEN_KEY)
        keyring.delete_password(
            self._keyring_client_name,
            self.KEYRING_REFRESH_TOKEN_KEY)

        if self.token is not None:
            keyring.set_password(
                self._keyring_client_name,
                self.KEYRING_TOKEN_KEY,
                self.__access_token)
        if self.refresh_token is not None:
            keyring.set_password(
                self._keyring_client_name,
                self.KEYRING_REFRESH_TOKEN_KEY,
                self.__refresh_token)
