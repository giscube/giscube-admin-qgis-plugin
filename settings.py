# -*- coding: utf-8 -*-
"""
This script contains the plugin's settings logic and defaults.
"""

from PyQt5.QtCore import QSettings

from .giscube_admin_configure_dialog import GiscubeAdminConfigureDialog


class Settings:
    ORGANIZATION = 'Microdisseny Giscube SLU'
    PROJECT = 'giscube-admin-qgis-plugin'

    SETTINGS_PREFIX = 'setting/'

    def __init__(self):
        self.__settings = QSettings(
            self.ORGANIZATION,
            self.PROJECT)

    def edit_popup(self):
        """
        Executes a popup that allows to modify the settings.
        """
        dialog = GiscubeAdminConfigureDialog(self)
        if dialog.exec_():
            self.save_connections = dialog.save_connections.isChecked()

    @property
    def save_connections(self):
        """
        Points if the new tokens should be saved.
        """
        return self.__settings.value(
            self.SETTINGS_PREFIX + 'save_connections',
            True,
            bool)

    @save_connections.setter
    def save_connections(self, value):
        return self.__settings.setValue(
            self.SETTINGS_PREFIX + 'save_connections',
            value)
