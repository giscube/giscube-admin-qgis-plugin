#!/usr/bin/env python
"""
Test units for the package backend.utils.
"""

from unittest import TestCase

from backend import utils


class TestUrljoin(TestCase):
    def test(self):
        self.assertEqual(utils.urljoin(''), '')

        self.assertEqual(
            utils.urljoin('https://server.example', 'level1', 'level2'),
            'https://server.example/level1/level2'
        )

        self.assertEqual(
            utils.urljoin('https://server.example/', '/level1/', '/level2/'),
            'https://server.example/level1/level2/'
        )

        self.assertEqual(
            utils.urljoin('file:///usr/bin/', 'level1', 'level2'),
            'file:///usr/bin/level1/level2'
        )
