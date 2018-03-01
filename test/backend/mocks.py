#!/usr/bin/env python
"""
File that contains all the mock classes for the unit test.
"""

import logging
import sys

from .constants import Test

from backend.constants import Oauth
from backend.utils import urljoin

logging.basicConfig()
logger = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MockResponse:
    """
    Class that imitates an requests.Response object for mocking porpuses.
    """
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        pass


def mocked_get(url, params):
    logger.debug('---------------------')
    logger.info('Mocked get')
    logger.debug(url)
    logger.debug(str(params))

    return MockResponse(None, 200)


def mocked_post(url, data):
    logger.debug('---------------------')
    logger.info('Mocked post')
    logger.debug(url)
    logger.debug(str(data))

    if url == urljoin(Test.URL, Oauth.PATH):
        logger.info('Post to oauth')
        return MockResponse({'access_token': 'test'}, 200)

    return MockResponse(None, 200)


def mocked_put(url, data):
    logger.info('---------------------')
    logger.info('Mocked put')
    logger.info(url)
    logger.debug(str(data))

    return MockResponse(None, 200)
