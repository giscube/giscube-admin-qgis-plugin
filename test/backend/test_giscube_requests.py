#!/usr/bin/env python
"""
Test units for the package backend.giscube_requests.
"""

from unittest import mock, TestCase

from .constants import Test
from backend.token_handler import TokenHandler
from backend.giscube_requests import GiscubeRequests, BadCredentials

from .mocks import mocked_get, mocked_post, mocked_put


class TestGiscubeRequests(TestCase):
    @classmethod
    @mock.patch('requests.post', mocked_post)
    def setUpClass(cls):
        handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)
        handler.login(Test.USER, Test.PASSWORD)
        cls._token_handler = handler

    @mock.patch('requests.get', mocked_get)
    @mock.patch('requests.post', mocked_post)
    @mock.patch('requests.put', mocked_put)
    def testBadCredentials(self):
        # token handler without any login
        token_handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)
        giscube = GiscubeRequests(token_handler)

        with self.assertRaises(BadCredentials):
            giscube.request_projects_list()

        with self.assertRaises(BadCredentials):
            giscube.request_project(Test.MOCK_PROJECT['id'])

        with self.assertRaises(BadCredentials):
            giscube.push_project(
                Test.MOCK_PROJECT['id'],
                Test.MOCK_PROJECT['name'],
                '')

    @mock.patch('requests.get', mocked_get)
    @mock.patch('requests.post', mocked_post)
    @mock.patch('requests.put', mocked_put)
    def testUpdateFile(self):
        giscube = GiscubeRequests(self._token_handler)
        projects_list = giscube.request_projects_list()
        project = next(iter(projects_list))  # Get frist project ID

        path = giscube.request_project(project)
        with open(path, 'r') as f:
            self.assertEqual(f.readline(), Test.MOCK_PROJECT['data'])

        giscube.push_project(project, Test.MOCK_PROJECT['name'], path)
        giscube.push_project(None, Test.MOCK_PROJECT['name'], path)
