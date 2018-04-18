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
            pass
