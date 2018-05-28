# -*- coding: utf-8 -*-
"""
This script contains LoginDialog: A dialog popup for the login credentials.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'login_dialog_base.ui'))


class LoginDialog(QtWidgets.QDialog, FORM_CLASS):
    """
    Popup dialog that ask for the necessary data to login into a server.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

    def values(self):
        values_dic = {
            'username': self.username.text(),
            'password': self.password.text(),
            'save_tokens': self.save_tokens.isChecked(),
        }
        return values_dic