#!/usr/bin/env python
"""
Test units for the package backend.giscube.
"""

from unittest import TestCase, mock

from .constants import Test
from backend.giscube import Giscube

from .mocks import mocked_post


class TestGiscube(TestCase):

    @mock.patch('requests.post', mocked_post)
    def test_properties(self):
        giscube = Giscube(Test.URL, Test.CLIENT_ID, False)
        self.assertEqual(giscube.server_url, Test.URL)
        self.assertEqual(giscube.client_id, Test.CLIENT_ID)

        self.assertFalse(giscube.is_logged_in)
        self.assertIsNone(giscube.access_token)
        self.assertFalse(giscube.has_refresh_token)

    @mock.patch('requests.post', mocked_post)
    def test_get_refresh(self):
        giscube = Giscube(Test.URL, Test.CLIENT_ID, False)

        self.assertFalse(giscube.is_logged_in)
        self.assertIsNone(giscube.access_token)
        self.assertFalse(giscube.has_refresh_token)

        giscube.login(Test.USER, Test.PASSWORD)

        self.assertTrue(giscube.is_logged_in)
        self.assertIsNotNone(giscube.access_token)

        if not giscube.has_refresh_token:
            return

        old_access_token = giscube.access_token

        giscube.refresh_token()
        self.assertTrue(giscube.is_logged_in)
        self.assertIsNotNone(giscube.access_token)

        self.assertNotEqual(old_access_token, giscube.access_token)

    @mock.patch('requests.post', mocked_post)
    def test_saving_loading(self):
        giscube = Giscube(
            Test.URL,
            Test.CLIENT_ID,
            True,
            Giscube.KEYRING_NAME+'-test')
        giscube.login(Test.USER, Test.PASSWORD)
        old_access_token = giscube.access_token
        del giscube

        giscube = Giscube(
            Test.URL,
            Test.CLIENT_ID,
            True,
            Giscube.KEYRING_NAME+'-test')
        self.assertEqual(giscube.access_token, old_access_token)

        giscube.delete_saved()
        del giscube

        giscube = Giscube(
            Test.URL,
            Test.CLIENT_ID,
            True,
            Giscube.KEYRING_NAME+'-test')

        self.assertFalse(giscube.is_logged_in)
        self.assertIsNone(giscube.access_token)
        self.assertFalse(giscube.has_refresh_token)
