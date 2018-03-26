# -*- coding: utf-8 -*-
"""
This script contains ProjectItem.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from qgis.core import QgsProject


class ProjectItem(QTreeWidgetItem):
    """
    Server instance on the plugin's server tree UI.
    Controlls the interaction with the user.
    """
    def __init__(self, id, name, server_item):
        """
        Contructor.
        """
        super().__init__()

        self.id = id
        self.name = name
        self.path = None

        self.server_item = server_item
        self.qgis_server = self.server_item.giscube.qgis_server
        self.iface = server_item.iface

        server_item.addChild(self)
        self.setText(0, self.name)

    def _double_clicked(self):
        def open_project():
            project = QgsProject.instance()
            self.path = self.qgis_server.download_project(self.id)
            project.read(self.path)
            project.readProject.connect(close_project)
            project.projectSaved.connect(save_project)

        def save_project():
            self.qgis_server.upload_project(
                self.id,
                self.name,
                self.path,
            )

        def close_project():
            project = QgsProject.instance()
            project.readProject.disconnect(close_project)
            project.projectSaved.disconnect(save_project)

        self.iface.newProjectCreated.connect(
            open_project,
            Qt.DirectConnection)
        self.iface.newProject(True)
        self.iface.newProjectCreated.disconnect(
            open_project)

    def context_menu(self, pos):
        pass
