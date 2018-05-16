# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminConfigureDialog.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_configure_dialog_base.ui'))


class GiscubeAdminConfigureDialog(QtWidgets.QDialog, FORM_CLASS):
    """
    Popup that allows the user to edit the necessary global settings of this
    plugin.
    """

    def __init__(self, settings, parent=None):
        """Constructor."""
        super(GiscubeAdminConfigureDialog, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Set current values
