# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminConfigureDialog: the class of the lateral dock
that opens with the plugin.
"""

import os

from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_configure_dialog_base.ui'))


class GiscubeAdminConfigureDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, settings, parent=None):
        """Constructor."""
        super(GiscubeAdminConfigureDialog, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Set current values
        self.save_connections.setChecked(settings.save_connections)
