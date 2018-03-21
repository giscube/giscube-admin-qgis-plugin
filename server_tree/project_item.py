# -*- coding: utf-8 -*-
"""
This script contains ProjectItem: The instance of a project UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem


class ProjectItem(QTreeWidgetItem):
    def __init__(self, id, name, server_item):
        super().__init__()

        self.id = id
        self.name = name
        self.server_item = server_item

        server_item.addChild(self)
        self.setText(0, self.name)

    def double_clicked(self):
        pass
