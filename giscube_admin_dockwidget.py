# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminDockWidget: the class of the lateral dock that opens with the plugin.
"""

import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_dockwidget_base.ui'))


class GiscubeAdminDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(GiscubeAdminDockWidget, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Add signals and slots connections
        self.loginSubmit.clicked.connect(self.__login)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def __login(self):
        pass # TODO actual login
