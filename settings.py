# -*- coding: utf-8 -*-
"""
This script contains the plugin's settings logic and defaults.
"""

from PyQt5.QtCore import QSettings


class Settings:
    def __init__(self):
        self.__settings = QSettings(
            'Microdisseny Giscube SLU',
            'giscube-admin-qgis-plugin')

    def edit_popup(self):
        """
        Executes a popup that allows to modify the settings.
        """
        pass

    @property
    def save_tokens(self):
        """
        Points if the new tokens should be saved.
        """
        return self.__settings.value('save_tokens', True, bool)

    @save_tokens.setter
    def set_save_tokens(self, v):
        return self.__settings.setValue('save_tokens', v)
