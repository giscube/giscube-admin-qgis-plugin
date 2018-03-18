# -*- coding: utf-8 -*-
"""
This script contains Server: The instance of the server UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton

from .project_item import ProjectItem


class ServerItem(QTreeWidgetItem):
    def __init__(self, name, conn, root):
        super(ServerItem, self).__init__()

        self.name = name
        self.giscube_conn = conn
        self.root = root

    def setupUI(self):
        self.setText(0, self.name)

        self.new_project = QPushButton('New Project')
        self.root.setItemWidget(self, 1, self.new_project)

        projects = self.giscube_conn.qgis_server.projects()
        for pid, name in projects.items():
            project = ProjectItem(pid, name, self.root)
            self.addChild(project)
            project.setupUI()
