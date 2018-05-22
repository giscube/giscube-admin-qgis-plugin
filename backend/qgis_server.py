#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""

import time
import requests

from PyQt5.QtCore import QDir

from .constants import Api
from .exceptions import Unauthorized
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
        self.giscube = giscube

    def projects(self):
        """
        Returns a list with all the projects available.

        :raise Unauthorized: When the request is not successful because the
        server didn't accept the credentials.
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.giscube.is_logged_in:
            raise Unauthorized()

        response = self.giscube.try_request(self.__request_projects_list)
        projects = {
            result['id']: result['name'] for result in response['results']
        }
        services = {
            r['id']: r['service'] for r in response['results'] if r['service']
        }
        return projects, services

    def download_project(self, project_id):
        """
        Downloads the project file.
        Returns the path of the file.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raise Unauthorized: When the request is not successful because the
        server didn't accept the credentials.
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.giscube.is_logged_in:
            raise Unauthorized()

        response = self.giscube.try_request(self.__request_project, project_id)

        t = '{:.0f}'.format(time.time())
        path = QDir.tempPath() + (
            '/qgis-admin-project-'+str(project_id)+'-'+t+'.qgs'
        )
        with open(path, 'w') as f:
            if 'data' in response:
                f.write(response['data'])

        return path

    def upload_project(self, project_id, title, path):
        """
        Uploads the project from a path to the server with project_name.
        Overrides it in the server if a project_id is given (there must exist a
        project with that ID).
        Returns the project ID.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :param title: Project's tile in the server.
        :type title: str
        :param path: Project's ID in the server.
        :type path: str or unicode
        :raise Unauthorized: When the request is not successful because the
        server didn't accept the credentials.
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        if not self.giscube.is_logged_in:
            raise Unauthorized()

        with open(path, 'r') as f:
            qgis_project = f.read()

        result = self.giscube.try_request(
            self.__push_project,
            project_id,
            title,
            qgis_project,
            process_result=False,
        )

        return result.json()['id']

    def delete_project(self, project_id):
        """
        Deletes a project from the server.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :raise Unauthorized: When the request is not successful because the
        server didn't accept the credentials.
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        self.giscube.try_request(
            self.__delete_project,
            project_id,
            process_result=False,
        )

    def publish_project(self, project_id,
                        title, description, keywords, on_geoportal,
                        category=None):
        """
        Publishes the project into a map service (or update the service data if
        it is already published).
        Returns the created service ID.

        :param project_id: Project's ID in the server.
        :type project_id: int or str
        :param title: Service's tile.
        :type title: str
        :param description: Service's description.
        :type description: str or unicode
        :param keywords: Comma separated list of keywords to add.
        :type keywords: str or unicode
        :param on_geoportal: Should it be published on the Geoportal?
        :type on_geoportal: bool
        :param category: Category of the publication.
        :type category: int or None
        :raise Unauthorized: When the request is not successful because the
        server didn't accept the credentials.
        :raises requests.exceptions.HTTPError: When the server responses with
        an unexpected error status code
        """
        result = self.giscube.try_request(
            self.__publish_project,
            project_id,
            title,
            description,
            keywords,
            on_geoportal,
            category,
        )
        return result["service"]

    def __request_projects_list(self):
        return requests.get(
            urljoin(
                self.giscube.server_url,
                Api.PATH,
                Api.PROJECTS),
            params={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
            }
        )

    def __request_project(self, project_id):
        return requests.get(
            urljoin(
                self.giscube.server_url,
                Api.PATH,
                Api.PROJECTS,
                project_id),
            params={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
            }
        )

    def __push_project(self, project_id, title, qgis_project):
        if project_id is None:  # if need to create a new project
            request = requests.post
            url = urljoin(
                self.giscube.server_url,
                Api.PATH,
                Api.PROJECTS,
            )
        else:
            request = requests.put
            url = urljoin(
                self.giscube.server_url,
                Api.PATH,
                Api.PROJECTS,
                str(project_id),
            )

        return request(
            url,
            data={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
                'id': project_id,
                'name': title,
                'data': qgis_project,
            }
        )

    def __delete_project(self, project_id):
        url = urljoin(
            self.giscube.server_url,
            Api.PATH,
            Api.PROJECTS,
            str(project_id),
        )

        return requests.delete(
            url,
            data={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
            }
        )

    def __publish_project(self, project_id,
                          title, description, keywords, on_geoportal,
                          category):
        url = urljoin(
            self.giscube.server_url,
            Api.PATH,
            Api.PROJECTS,
            str(project_id),
            Api.PUBLISH,
        )
        return requests.post(
            url,
            data={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
                'name': "project",
                'title': title,
                'description': description,
                'keywords': keywords,
                'visible_on_geoportal': on_geoportal,
                'category': category,
            }
        )
