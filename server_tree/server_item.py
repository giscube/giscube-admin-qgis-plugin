# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton

from .loading_item import LoadingItem


class ServerItem(QTreeWidgetItem):
    def __init__(self, conn, tree_widget):
        super().__init__()

        self._giscube_conn = conn

        tree_widget.addTopLevelItem(self)

        self.setText(0, self.name)

        self.new_project = QPushButton('New Project')
        tree_widget.setItemWidget(self, 1, self.new_project)

        self.addChild(LoadingItem())

    @property
    def name(self):
        return self._giscube_conn.name

    @property
    def server_url(self):
        self._giscube_conn.server_url

    @property
    def save_tokens(self):
        self._giscube_conn.save_tokens

    def expanded(self):
        if self.childCount() == 1 and isinstance(self.child(0), LoadingItem):
            pass  # TODO load projects
