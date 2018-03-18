# -*- coding: utf-8 -*-
"""
This script contains the plugin's settings logic and defaults.
"""

from PyQt5.QtCore import QSettings

from .giscube_admin_configure_dialog import GiscubeAdminConfigureDialog


class Settings:
    def __init__(self):
        self.__settings = QSettings(
            'Microdisseny Giscube SLU',
            'giscube-admin-qgis-plugin')

    def edit_popup(self):
        """
        Executes a popup that allows to modify the settings.
        """
        dialog = GiscubeAdminConfigureDialog(self)
        if dialog.exec_():
            print(dialog.save_connections.isChecked())
            self.save_connections = dialog.save_connections.isChecked()

    @property
    def save_connections(self):
        """
        Points if the new tokens should be saved.
        """
        return self.__settings.value('save_connections', True, bool)

    @save_connections.setter
    def save_connections(self, v):
        return self.__settings.setValue('save_connections', v)
