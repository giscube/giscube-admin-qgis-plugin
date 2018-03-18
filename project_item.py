# -*- coding: utf-8 -*-
"""
This script contains Server: The instance of the project UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem


class ProjectItem(QTreeWidgetItem):
    def __init__(self, id, name, root):
        super(ProjectItem, self).__init__()

        self.id = id
        self.name = name

    def setupUI(self):
        self.setText(0, self.name)
