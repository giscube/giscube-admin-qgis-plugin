#!/usr/bin/env python
"""
Test units for the package backend.giscube_requests.
"""

from unittest import TestCase

from .constants import Test
from backend.token_handler import TokenHandler
from backend.giscube_requests import GiscubeRequests, BadCredentials


class TestGiscubeRequests(TestCase):
    @classmethod
    def setUpClass(cls):
        handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)
        handler.login(Test.USER, Test.PASSWORD)
        cls._token_handler = handler

    def testBadCredentials(self):
        # token handler without any login
        token_handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)
        giscube = GiscubeRequests(token_handler)

        with self.assertRaises(BadCredentials):
            giscube.request_projects_list()

        with self.assertRaises(BadCredentials):
            giscube.request_project(Test.MOCK_PROJECT)

        with self.assertRaises(BadCredentials):
            giscube.push_project(Test.MOCK_PROJECT, 'fail', '')

    def testUpdateFile(self):
        giscube = GiscubeRequests(self._token_handler)
        projects_list = giscube.request_projects_list()
        project = next(iter(projects_list))  # Get frist project ID

        path = giscube.request_project(project)
        with open(path, 'r') as f:
            self.assertEqual(f.readline(), 'Mock OK')

        giscube.push_project(project, 'mock_project.qgs', path)
