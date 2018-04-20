# -*- coding: utf-8 -*-
"""
This script contains ProjectItem.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction, QTreeWidgetItem, QPushButton

from qgis.core import QgsProject

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
        self.published = published

        self.server_item = server_item
        self.qgis_server = self.server_item.giscube.qgis_server
        self.iface = server_item.iface

        server_item.addChild(self)
        self.setText(0, self.name)

        self.publish = QPushButton('Publish')
        server_item.treeWidget().setItemWidget(self, 1, self.publish)
        self.publish.clicked.connect(
            lambda: self._publish_popup()
            )

    def open(self):
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

        self.iface.newProjectCreated.connect(
            open_project,
            Qt.DirectConnection)
        self.iface.newProject(True)
        self.iface.newProjectCreated.disconnect(
            open_project)

    def _double_clicked(self):
        self.open()

    def context_menu(self, pos):
        menu = QMenu()

        # def refresh():
        #     main_company.list_job(ListProjectsJob(self))
        # refresh_action = QAction('&Refresh projects')
        # menu.addAction(refresh_action)
        # refresh_action.triggered.connect(refresh)

        # def close():
        #     self.delete()
        # close_action = QAction('&Close connection')
        # menu.addAction(close_action)
        # close_action.triggered.connect(close)

        def open_():
            self.open()
        open_action = QAction('&Open project')
        menu.addAction(open_action)
        open_action.triggered.connect(open_)

        def delete():
            self.qgis_server.delete_project(self.id)
            self.server_item.removeChild(self)
        delete_action = QAction('&Delete project')
        menu.addAction(delete_action)
        delete_action.triggered.connect(delete)

        menu.exec_(pos)

    def _publish_popup(self):
        dialog = PublishDialog(self.name, self.published)
        if dialog.exec_():
            published = self.qgis_server.publish_project(
                self.id,
                **dialog.values()
            )
            self.published = published
