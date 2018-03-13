#!/usr/bin/env python
"""
Test units for the package backend.qgis_server.
"""

from unittest import mock, TestCase

from .constants import Test
from backend.exceptions import Unauthorized
from backend.giscube import Giscube

from .mocks import mocked_get, mocked_post, mocked_put


class TestGiscubeRequests(TestCase):
    @classmethod
    @mock.patch('requests.post', mocked_post)
    def setUpClass(cls):
        giscube = Giscube(Test.URL, Test.CLIENT_ID, False)
        giscube.login(Test.USER, Test.PASSWORD)
        cls._giscube = giscube

    @mock.patch('requests.get', mocked_get)
    @mock.patch('requests.post', mocked_post)
    @mock.patch('requests.put', mocked_put)
    def testUnauthorized(self):
        # token handler without any login
        giscube = Giscube(Test.URL, Test.CLIENT_ID, False)
        qgis_server = giscube.qgis_server

        with self.assertRaises(Unauthorized):
            qgis_server.projects()

        with self.assertRaises(Unauthorized):
            qgis_server.download_project(Test.MOCK_PROJECT['id'])

        with self.assertRaises(Unauthorized):
            qgis_server.upload_project(
                Test.MOCK_PROJECT['id'],
                Test.MOCK_PROJECT['name'],
                '')

    @mock.patch('requests.get', mocked_get)
    @mock.patch('requests.post', mocked_post)
    @mock.patch('requests.put', mocked_put)
    def testUpdateFile(self):
        qgis_server = self._giscube.qgis_server
        projects_list = qgis_server.projects()
        project = next(iter(projects_list))  # Get frist project ID

        path = qgis_server.download_project(project)
        with open(path, 'r') as f:
            self.assertEqual(f.readline(), Test.MOCK_PROJECT['data'])

        qgis_server.upload_project(project, Test.MOCK_PROJECT['name'], path)
        qgis_server.upload_project(None, Test.MOCK_PROJECT['name'], path)
