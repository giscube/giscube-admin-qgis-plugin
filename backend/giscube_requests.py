#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""
from urllib.parse import urljoin

from PyQt5.QtCore import QDir
import requests


class BadCredentials(ConnectionError):
    """
    The credentials or the token used are wrong or have expired.
    """
    pass


class GiscubeRequests:  # TODO do all the https requests
    """
    Handles all the requests to the Giscube server. May return a BadCredentials
    error.
    """
    def __init__(self, token_handler):
        self.__token_handler = token_handler

    def request_projects_list(self):
        """
        Returns a list with all the projects. May return a BadCredentials
        error.
        """
        return []

    def request_project(self, project_id):
        """
        Downloads the project file and returns its path.
        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raises requests.exceptions.HTTPError: when the server responses with
        an unexpected error status code
        """
        path = QDir.tempPath() + '/qgis-admin-project-'+project_id+'.qgs'
        response = requests.get(
            urljoin(
                self.__token_handler.server_url,
                'projects',
                project_id),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            })
        response_object = response.json()

        # TODO: add expected errors checking
        response.raise_for_status()

        with open(path, 'w') as f:

            if 'data' in response_object:  # TODO: add type checking
                f.write(response_object['data'])

        return path

    def push_project(self, path, title, project_id):
        """
        Saves the project in a path to the server with project_name overriding
        it if exists. May return a BadCredentials error.
        :param path: Project's ID in the server.
        :type path: str or unicode
        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raises requests.exceptions.HTTPError: when the server responses with
        an unexpected error status code
        """
        try:
            f = open(path, 'r')
            qgis_project = f.read()
            f.close()
        except:
            return False

        response = requests.put(
            urljoin(
                self.__token_handler.server_url,
                'projects',
                project_id),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            },
            data={
                'title': title,
                'data': qgis_project,
            })

        # TODO: Add exepected errors
        response.raise_for_status()

        return True
