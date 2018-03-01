#!/usr/bin/env python
"""
File that contains all the mock classes for the unit test.
"""

import logging
import sys

from .constants import Test

from backend.constants import Oauth, Api
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

    projects_path = urljoin(Test.URL, Api.PATH, Api.PROJECTS)
    if url == projects_path:
        logger.info('Get to api/projects')
        if 'access_token' in params and params['access_token'] is not None:
            data = {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [Test.MOCK_PROJECT, ]}
            return MockResponse(data, 200)
        else:
            return MockResponse({}, Api.BAD_CREDENTIALS)

    elif url.startswith(projects_path):
        if 'access_token' in params and params['access_token'] is not None:
            return MockResponse(Test.MOCK_PROJECT, 200)
        else:
            return MockResponse({}, Api.BAD_CREDENTIALS)


def mocked_post(url='', params='', data=''):
    logger.debug('---------------------')
    logger.info('Mocked post')
    logger.debug(url)
    logger.debug(str(params))
    logger.debug(str(data))

    if url == urljoin(Test.URL, Oauth.PATH):
        logger.info('Post to oauth')
        return MockResponse({'access_token': 'test'}, 200)

    if url == urljoin(Test.URL, Api.PATH, Api.PROJECTS):
        if 'access_token' in params and params['access_token'] is not None:
            return MockResponse({}, 200)
        else:
            return MockResponse({}, Api.BAD_CREDENTIALS)


def mocked_put(url='', params='', data=''):
    logger.info('---------------------')
    logger.info('Mocked put')
    logger.info(url)
    logger.debug(str(params))
    logger.debug(str(data))

    projects_path = urljoin(Test.URL, Api.PATH, Api.PROJECTS)
    if url.startswith(projects_path):
        if 'access_token' in params and params['access_token'] is not None:
            return MockResponse({}, 200)
        else:
            return MockResponse({}, Api.BAD_CREDENTIALS)
