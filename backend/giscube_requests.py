#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the
Giscube server.
"""
import re

from PyQt5.QtCore import QDir
import requests


def urljoin(base, *parts):
    """
    Joins the base and the parts separating them with a slash. Removes
    duplicated slashes except if is part of the protocol (ie. https://).
    :param base: Base url.
    :type base: str
    """
    result = base
    for part in parts:
        result += '/'+part
    result = re.sub(
        r'(?<!/)(?<!:)/{2,}',
        '/',
        result)
    return result


class BadCredentials(ConnectionError):
    """
    The credentials or the token used are wrong or have expired.
    """
    pass


class GiscubeRequests:
    """
    Handles all the requests to the Giscube server. May return a BadCredentials
    error.
    """
    API_PATH = 'api/v1'
    API_PROJECTS = 'projects'

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
                self.API_PATH,
                self.API_PROJECTS),
            params={
                'client_id': self.__token_handler.client_id,
                'access_token': self.__token_handler.access_token,
            })
        # TODO: add expected errors checking
        response.raise_for_status()

        response_object = response.json()
        # if 'results' in response_object:
        projects = []  # TODO Maybe another container would work better
        for entry in response_object['results']:
            project = (entry['id'], entry['name'])
            projects.append(project)

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
                self.API_PATH,
                self.API_PROJECTS,
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
                self.API_PATH,
                self.API_PROJECTS)
        else:
            request = requests.put
            url = urljoin(
                self.__token_handler.server_url,
                self.API_PATH,
                self.API_PROJECTS,
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
