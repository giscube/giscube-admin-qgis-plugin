#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""

from PyQt5.QtCore import QDir
import requests

from .constants import GiscubeApi as Api
from .utils import urljoin


class BadCredentials(ConnectionError):
    """
    The credentials or the token used are wrong or have expired.
    """
    pass


class ExpiredToken(ConnectionError):
    """
    The token has expired.
    """
    pass


class GiscubeRequests:
    """
    Handles all the requests to the Giscube server. May return a BadCredentials
    error.
    """

    def __init__(self, token_handler):
        self.__token_handler = token_handler

    def request_projects_list(self):
        """
        Returns a list with all the projects.
        :raises requests.exceptions.HTTPError: when the server responses with
        an unexpected error status code
        """
        response = requests.get(
            urljoin(
                self.__token_handler.server_url,
                Api.PATH,
                Api.PROJECTS),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            })
        # TODO: add expected errors checking
        response.raise_for_status()

        response_object = response.json()
        # if 'results' in response_object:
        # TODO Maybe another container would work better
        projects = {
            result['id']: result['title']
            for result in response_object['result']}
        return projects

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
                Api.PATH,
                Api.PROJECTS,
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

        if project_id is None:  # if need to create a new project
            request = requests.post
            url = urljoin(
                self.__token_handler.server_url,
                Api.PATH,
                Api.PROJECTS)
        else:
            request = requests.put
            url = urljoin(
                self.__token_handler.server_url,
                Api.PATH,
                Api.PROJECTS,
                project_id)

        response = request(
            url,
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
