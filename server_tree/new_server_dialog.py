# -*- coding: utf-8 -*-
"""
This script contains NewServerDialog.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'new_server_dialog_base.ui'))


class NewServerDialog(QtWidgets.QDialog, FORM_CLASS):
    """
    Popup dialog that ask for the necessary data to make a new server
    connection.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

    def values(self):
        values_dic = {
            'name': self.name.text(),
            'url': self.url.text(),
        }
        return values_dic
