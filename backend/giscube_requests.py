#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""

from PyQt5.QtCore import QDir
import requests

from .constants import Api
from .utils import urljoin


class BadCredentials(ConnectionError):
    """
    The credentials or the token used are wrong or have expired and cannot be
    refreshed.
    """
    pass


class GiscubeRequests:
    """
    Handles all the requests to the Giscube server. May return a BadCredentials
    error.
    """

    def __init__(self, token_handler):
        """
        Constructor.

        :param token_handler: Object that handles the tokens.
        :type token_handler: backend.TokenHandler
        """
        self.__token_handler = token_handler

    def request_projects_list(self):
        """
        Returns a list with all the projects.

        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        response = self.__get_result(self.__make_request_projects_list)
        projects = {
            result['id']: result['title'] for result in response['result']
        }
        return projects

    def request_project(self, project_id):
        """
        Downloads the project file and returns its path.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        response = self.__get_result(self.__make_request_project, project_id)

        path = QDir.tempPath() + '/qgis-admin-project-'+project_id+'.qgs'
        with open(path, 'w') as f:
            if 'data' in response:
                f.write(response['data'])

        return path

    def push_project(self, path, title, project_id):
        """
        Saves the project from a path to the server with project_name.
        Overrides it in the server if a project_id is given.

        :param path: Project's ID in the server.
        :type path: str or unicode
        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        with open(path, 'r') as f:
            qgis_project = f.read()

        self.__get_result(
            self.__make_push_project,
            project_id,
            title,
            qgis_project,
            process_result=False,
        )

    def __get_result(self, make_request, *args, process_result=True):
        """
        Tries to get the a request result.

        It makes the request (which must be a function that returns the
        result). If it fails, it tries to refresh the token and tries again.

        Returns the parsed json object.

        :param make_request: request function
        :type request: method
        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        response = make_request(*args)
        if response.status_code == Api.BAD_CREDENTIALS:
            if not self.__token_handler.has_refresh_token:
                raise BadCredentials()

            self.__token_handler.refresh_token()

            response = make_request(*args)
            if response.status_code == Api.BAD_CREDENTIALS:
                raise BadCredentials()

        response.raise_for_status()

        if process_result:
            return response.json()
        else:
            return response

    def __make_request_projects_list(self):
        """
        Function that performs the request to get the list of projects.
        """
        return requests.get(
            urljoin(
                self.__token_handler.server_url,
                Api.PATH,
                Api.PROJECTS),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            }
        )

    def __make_request_project(self, project_id):
        """
        Function that requests the server for an specific project.
        """
        return requests.get(
            urljoin(
                self.__token_handler.server_url,
                Api.PATH,
                Api.PROJECTS,
                project_id),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            }
        )

    def __make_push_project(self, project_id, title, qgis_project):
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
                project_id+'/')

        return request(
            url,
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            },
            data={
                'title': title,
                'data': qgis_project,
            }
        )
