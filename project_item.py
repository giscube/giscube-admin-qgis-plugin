# -*- coding: utf-8 -*-
"""
This script contains Server: The instance of the project UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem


class ProjectItem(QTreeWidgetItem):
    def __init__(self, id, name, root, giscube_conn):
        super(ProjectItem, self).__init__()

        self.id = id
        self.name = name
        self.root = root
        self.giscube_conn = giscube_conn

    def setupUI(self):
        self.setText(0, self.name)

    def double_clicked(self):
        pass
