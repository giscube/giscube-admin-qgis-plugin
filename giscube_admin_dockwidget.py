# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminDockWidget: the class of the lateral dock that
opens with the plugin.
"""

import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

from .tree_controller import TreeController

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_dockwidget_base.ui'))


class GiscubeAdminDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(GiscubeAdminDockWidget, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.servers.setColumnWidth(0, 210)

        self.tree_controller = TreeController(self.servers)

        # Add signals and slots connections
        self.new_server.clicked.connect(plugin.new_server_popup)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
