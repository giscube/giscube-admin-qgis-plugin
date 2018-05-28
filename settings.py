# -*- coding: utf-8 -*-
"""
This script contains the plugin's settings logic and defaults.
"""

from PyQt5.QtCore import QSettings

from .ui.giscube_admin_configure_dialog import GiscubeAdminConfigureDialog


class Settings:
    ORGANIZATION = 'Giscube'
    PROJECT = 'giscube-admin-qgis-plugin'

    SETTINGS_PREFIX = 'setting/'
    UI_PREFIX = 'ui/'

    IS_OPEN_SETTING = SETTINGS_PREFIX + UI_PREFIX + 'is_open'

    def __init__(self):
        self.__settings = QSettings(
            self.ORGANIZATION,
            self.PROJECT)

    @property
    def is_open(self):
        v = self.__settings.value(self.IS_OPEN_SETTING, 'f')
        if isinstance(v, str):
            return v[0] in ['t', 'T']
        else:
            return v

    @is_open.setter
    def is_open(self, v):
        self.__settings.setValue(self.IS_OPEN_SETTING, v)
        self.__settings.sync()

    def edit_popup(self):
        """
        Executes a popup that allows to modify the settings.
        """
        dialog = GiscubeAdminConfigureDialog(self)
        if dialog.exec_():
            pass
