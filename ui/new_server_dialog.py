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
    Popup dialog that asks for the necessary data to make a new server
    connection.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

    def values(self):
        """
        Returns a dictionary with the values of this dialog's widgets.
        """
        values_dic = {
            'name': self.name.text(),
            'url': self.url.text(),
            'username': self.username.text(),
            'password': self.password.text(),
            'save_tokens': not self.discard_tokens.isChecked(),
        }
        return values_dic
