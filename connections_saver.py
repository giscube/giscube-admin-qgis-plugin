# -*- coding: utf-8 -*-
"""
This script contains the class ConnectionsSaver: saves what connections are
open.
"""

import json

from PyQt5.QtCore import QSettings

from .settings import Settings


class ConnectionsSaver:
    CONNECTIONS_PREFIX = 'connections/'

    def __init__(self):
        self.settings = QSettings(
            Settings.ORGANIZATION,
            Settings.PROJECT)

    @property
    def connections(self):
        json_repr = self.settings.value(
            self.CONNECTIONS_PREFIX+'server_conections',
            '[]')
        return json.loads(json_repr)

    @connections.setter
    def connections(self, value):
        json_repr = json.dumps(value)
        self.settings.setValue(
            self.CONNECTIONS_PREFIX+'server_conections',
            json_repr)
