#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""

from PyQt5.QtCore import QDir
import requests

from .constants import Api
from .exceptions import BadCredentials
from .utils import urljoin


class QgisServer:
    """
    Giscube's QGis Server API client.
    """

    def __init__(self, giscube):
        """
        Constructor.

        :param token_handler: Main Giscube API client.
        :type token_handler: backend.Giscube
        """
        self.__giscube = giscube

    def projects(self):
        """
        Returns a list with all the projects available.

        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.__giscube.is_logged_in:
            raise BadCredentials()

        response = self.__get_result(self.__request_projects_list)
        projects = {
            result['id']: result['name'] for result in response['results']
        }
        return projects

    def download_project(self, project_id):
        """
        Downloads the project file and returns its path.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.__giscube.is_logged_in:
            raise BadCredentials()

        response = self.__get_result(self.__request_project, project_id)

        path = QDir.tempPath() + '/qgis-admin-project-'+str(project_id)+'.qgs'
        with open(path, 'w') as f:
            if 'data' in response:
                f.write(response['data'])

        return path

    def upload_project(self, project_id, title, path):
        """
        Uploads the project from a path to the server with project_name.
        Overrides it in the server if a project_id is given (there must exist a
        project with that ID).

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :param title: Project's tile in the server.
        :type title: str
        :param path: Project's ID in the server.
        :type path: str or unicode
        :raise BadCredentials: When the servers negates the credentials,
        preventing to do the request
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.__giscube.is_logged_in:
            raise BadCredentials()

        with open(path, 'r') as f:
            qgis_project = f.read()

        self.__get_result(
            self.__push_project,
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
            if not self.__giscube.has_refresh_token:
                raise BadCredentials()

            self.__giscube.refresh_token()

            response = make_request(*args)
            if response.status_code == Api.BAD_CREDENTIALS:
                raise BadCredentials()

        response.raise_for_status()

        if process_result:
            return response.json()
        else:
            return response

    def __request_projects_list(self):
        return requests.get(
            urljoin(
                self.__giscube.server_url,
                Api.PATH,
                Api.PROJECTS),
            params={
                'client_id': self.__giscube.client_id,
                'access_token': self.__giscube.access_token,
            }
        )

    def __request_project(self, project_id):
        return requests.get(
            urljoin(
                self.__giscube.server_url,
                Api.PATH,
                Api.PROJECTS,
                project_id),
            params={
                'client_id': self.__giscube.client_id,
                'access_token': self.__giscube.access_token,
            }
        )

    def __push_project(self, project_id, title, qgis_project):
        if project_id is None:  # if need to create a new project
            request = requests.post
            url = urljoin(
                self.__giscube.server_url,
                Api.PATH,
                Api.PROJECTS)
        else:
            request = requests.put
            url = urljoin(
                self.__giscube.server_url,
                Api.PATH,
                Api.PROJECTS,
                str(project_id)+'/')

        return request(
            url,
            params={
                'client_id': self.__giscube.client_id,
                'access_token': self.__giscube.access_token,
            },
            data={
                'title': title,
                'data': qgis_project,
            }
        )