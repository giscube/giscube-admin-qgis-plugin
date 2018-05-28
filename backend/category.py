#!/usr/bin/env python

import requests

from .constants import Api
from .utils import urljoin


class Category:
    """
    Defines a single category on the giscube server.
    """
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent


class CategoryApi:
    def __init__(self, giscube):
        self.giscube = giscube

    def get_categories(self):
        """
        Downloads the categories from the server.
        """
        categories = {}
        json = self.giscube.try_request(self._get_categories)
        for o in json:
            categories[o['id']] = Category(o['name'], o['parent'])
        return categories

    def _get_categories(self):
        return requests.get(
            urljoin(
                self.giscube.server_url,
                Api.PATH,
                Api.CATEGORY),
            params={
                'client_id': self.giscube.client_id,
                'access_token': self.giscube.access_token,
            }
        )
