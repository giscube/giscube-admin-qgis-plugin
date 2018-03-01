#!/usr/bin/env python
"""
Test units for the package backend.token_handler.
"""

from unittest import TestCase

from .constants import Test
from backend.token_handler import TokenHandler


class TestTokenHandler(TestCase):

    def test_properties(self):
        handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)
        self.assertEqual(handler.server_url, Test.URL)
        self.assertEqual(handler.client_id, Test.CLIENT_ID)

        self.assertFalse(handler.has_access_token)
        self.assertIsNone(handler.access_token)
        self.assertFalse(handler.has_refresh_token)

    def test_get_refresh(self):
        handler = TokenHandler(Test.URL, Test.CLIENT_ID, False)

        self.assertFalse(handler.has_access_token)
        self.assertIsNone(handler.access_token)
        self.assertFalse(handler.has_refresh_token)

        handler.login(Test.USER, Test.PASSWORD)

        self.assertTrue(handler.has_access_token)
        self.assertIsNotNone(handler.access_token)

        if not handler.has_refresh_token:
            return

        old_access_token = handler.access_token

        handler.refresh_token()
        self.assertTrue(handler.has_access_token)
        self.assertIsNotNone(handler.access_token)

        self.assertNotEqual(old_access_token, handler.access_token)

    def test_saving_loading(self):
        handler = TokenHandler(
            Test.URL,
            Test.CLIENT_ID,
            True,
            TokenHandler.KEYRING_APP_NAME+'-test')
        handler.login(Test.USER, Test.PASSWORD)
        old_access_token = handler.access_token
        del handler

        handler = TokenHandler(
            Test.URL,
            Test.CLIENT_ID,
            True,
            TokenHandler.KEYRING_APP_NAME+'-test')
        self.assertEqual(handler.access_token, old_access_token)

        handler.delete_saved()
        del handler

        handler = TokenHandler(
            Test.URL,
            Test.CLIENT_ID,
            True,
            TokenHandler.KEYRING_APP_NAME+'-test')

        self.assertFalse(handler.has_access_token)
        self.assertIsNone(handler.access_token)
        self.assertFalse(handler.has_refresh_token)
