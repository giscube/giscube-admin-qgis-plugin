#!/usr/bin/env python
"""
Package containing the Giscube API client.
"""

import requests
import keyring

from .constants import OAuth, Vault
from .utils import urljoin
from .qgis_server import QgisServer


class Giscube:
    """
    Giscube API client.
    Handles the login and recived token. It can be saved in a vault.
    """
    KEYRING_PREFIX = "giscube-admin-qgis-plugin-"

    def __init__(
            self,
            server_url,
            client_id,
            save_tokens=True,
            name=''):
        """
        Contructor. Loads, if enabled, the saved tokens.
        :param server_url: Used server service URL
        :type server_url: str
        :param client_id: Application OAuth client ID
        :type client_id: str or unicode
        :param save_tokens: Enables saving the tokens in a local vault
        :type save_tokens: bool
        """

        self._server_url = server_url
        self._client_id = client_id
        self.__access_token = None
        self.__refresh_token = None

        self.__qgis_server = None

        self._save = save_tokens
        self.__name = name
        self._keyring_client_name = self.KEYRING_PREFIX + name

        self.__load_tokens()

    @property
    def name(self):
        return self.__name

    @name.setter
    def set_name(self, name):
        self.delete_saved()
        self.__name = name
        self.__save_tokens()

    @property
    def qgis_server(self):
        """
        Giscube's QGis Server API client.
        """
        if self.__qgis_server is None:
            self.__qgis_server = QgisServer(self)

        return self.__qgis_server

    @property
    def server_url(self):
        """
        Base URL of the server.
        """
        return self._server_url

    @property
    def client_id(self):
        """
        Gets the client ID for this client, for this server.
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
        Current access token.
        """
        return self.__access_token

    @property
    def has_refresh_token(self):
        """
        Does it have a refresh token?
        """
        return self.__refresh_token is not None

    @property
    def is_logged_in(self):
        """
        Is the user logged in?
        """
        return self.has_access_token

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
            urljoin(self._server_url, OAuth.PATH),
            data={
                'username': user,
                'password': password,
                'grant_type': 'password',
                'client_id': self._client_id,
            }
        )

        if response.status_code == OAuth.UNAUTHORIZED:
            return False
        response.raise_for_status()
        response_object = response.json()

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
            urljoin(self._server_url, OAuth.PATH),
            data={
                'refresh-token': self.refresh_token,
                'grant_type': 'refresh_token',
                'client_id': self._client_id,
            }
        )

        if response.status_code == OAuth.UNAUTHORIZED:
            return False

        response.raise_for_status()
        response_object = response.json()

        token = response_object['access_token']
        refresh_token = response_object['refresh_token']

        self.__token = token
        self.__refresh_token = refresh_token
        self.__saveTokens()

        return True

    def __load_tokens(self):
        """
        Loads the tokens from a safe place.
        """
        if not self._save:
            return

        self.__access_token = keyring.get_password(
            self._keyring_client_name,
            Vault.ACCESS_TOKEN_KEY,
        )
        self.__refresh_token = keyring.get_password(
            self._keyring_client_name,
            Vault.REFRESH_TOKEN_KEY,
        )

    def __save_tokens(self):
        """
        Saves the tokens in a safe place (locally).
        """
        if not self._save:
            return

        self.delete_saved()

        if self.has_access_token:
            keyring.set_password(
                self._keyring_client_name,
                Vault.ACCESS_TOKEN_KEY,
                self.__access_token,
            )
        if self.has_refresh_token:
            keyring.set_password(
                self._keyring_client_name,
                Vault.REFRESH_TOKEN_KEY,
                self.__refresh_token,
            )

    def delete_saved(self):
        """
        Deletes the locally saved tokens (if they are).
        """
        try:
            keyring.delete_password(
                self._keyring_client_name,
                Vault.ACCESS_TOKEN_KEY,
            )
        except:
            pass

        try:
            keyring.delete_password(
                self._keyring_client_name,
                Vault.REFRESH_TOKEN_KEY,
            )
        except:
            pass
