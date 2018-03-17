# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminLoginDialog: A dialog that asks the user for
the logging credentials.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_login_dialog_base.ui'))


class GiscubeAdminLoginDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(GiscubeAdminLoginDialog, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)
