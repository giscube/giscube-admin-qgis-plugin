# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminDockWidget: the class of the lateral dock that
opens with the plugin.
"""

import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from .tree_controller import TreeController
from .server_item import ServerItem
from .project_item import ProjectItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_dockwidget_base.ui'))


class GiscubeAdminDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    """
    Plugin's main widget.
    """
    closingPlugin = pyqtSignal()

    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(GiscubeAdminDockWidget, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Set icons
        self.new_server.setIcon(QIcon(os.path.join(
            os.path.dirname(__file__),
            'resources',
            'new_server.svg'
        )))
        self.refresh.setIcon(QIcon(os.path.join(
            os.path.dirname(__file__),
            'resources',
            'refresh.svg'
        )))
        self.new_project.setIcon(QIcon(os.path.join(
            os.path.dirname(__file__),
            'resources',
            'new_project.svg'
        )))
        self.publish.setIcon(QIcon(os.path.join(
            os.path.dirname(__file__),
            'resources',
            'publish_project.svg'
        )))

        self.servers.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tree_controller = TreeController(self.servers)

        self.servers.itemSelectionChanged.connect(lambda: self.selectedEvent())

        def controlled_collapsed(index):
            current = self.servers.itemFromIndex(index)
            if current.indexOfChild(self.selected()) >= 0:
                self.servers.clearSelection()
                self.update_ui()

        self.servers.collapsed.connect(controlled_collapsed)

        # Add signals and slots connections
        self.new_server.clicked.connect(plugin.new_server_popup)

        self.refresh.clicked.connect(
            lambda: self.selected(ServerItem).refresh_projects())
        self.new_project.clicked.connect(
            lambda: self.selected(ServerItem).new_project_dialog())
        self.publish.clicked.connect(
            lambda: self.selected(ProjectItem)._publish_popup())

    def selected(self, c=None):
        selection = self.servers.selectedItems()
        if len(selection) == 1:
            selection = selection[0]
            if c is not None:
                while not isinstance(selection, c):
                    if isinstance(selection, ServerItem):
                        return None
                    selection = selection.parent()
            return selection
        return None

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def selectedEvent(self):
        status = 0
        selected = self.selected()
        if selected is not None:
            if isinstance(selected, ServerItem):
                status = 1
            elif isinstance(selected, ProjectItem):
                status = 2
        self.update_ui(status)

    def update_ui(self, status=0):
        self.refresh.setEnabled(status > 0)
        self.new_project.setEnabled(status > 0)
        self.publish.setEnabled(status > 1)
