# -*- coding: utf-8 -*-
"""
This script contains ProjectItem.
"""

from PyQt5.QtWidgets import QMenu, QAction, QTreeWidgetItem, QMessageBox

from qgis.core import QgsProject

from ..utils import safe_close, str2int

from .publish_dialog import PublishDialog


class ProjectItem(QTreeWidgetItem):
    """
    Server instance on the plugin's server tree UI.
    Controlls the interaction with the user.
    """
    def __init__(self, id, name, server_item, published=None):
        """
        Contructor.
        """
        super().__init__()

        self.id = id
        self.name = name
        self.path = None
        self.published = published or {}

        self.server_item = server_item
        self.qgis_server = self.server_item.giscube.qgis_server
        self.iface = server_item.iface

        server_item.addChild(self)
        self.setText(0, self.name)

    def open(self):
        """
        Open the project that this item represents in the editor.
        """
        def open_project():
            project = QgsProject.instance()
            self.path = self.qgis_server.download_project(self.id)
            project.read(self.path)
            project.readProject.connect(close_project)
            project.projectSaved.connect(save_project)

        def save_project():
            self.id = self.qgis_server.upload_project(
                self.id,
                self.name,
                self.path,
            )

        def close_project():
            project = QgsProject.instance()
            project.readProject.disconnect(close_project)
            project.projectSaved.disconnect(save_project)

        safe_close(self.iface, open_project)

    def _double_clicked(self):
        self.open()

    def context_menu(self, pos):
        menu = QMenu()

        def open_():
            self.open()
        open_action = QAction('&Open project')
        menu.addAction(open_action)
        open_action.triggered.connect(open_)

        def delete():
            confirm_dialog = QMessageBox(
                QMessageBox.Question,
                "Confirm project delete",
                "Do you really want to delete this project?\n"
                "It will be removed forever",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm_dialog.exec_() == QMessageBox.Yes:
                self.qgis_server.delete_project(self.id)
                self.server_item.removeChild(self)
        delete_action = QAction('Delete project')
        menu.addAction(delete_action)
        delete_action.triggered.connect(delete)

        menu.exec_(pos)

    def _publish_popup(self):
        dialog = PublishDialog(self)
        if dialog.exec_():
            published = self.qgis_server.publish_project(
                self.id,
                **dialog.values()
            )
            published['category'] = str2int(published['category'])
            self.published = published
