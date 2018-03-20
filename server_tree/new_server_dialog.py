# -*- coding: utf-8 -*-
"""
This script contains NewServerDialog: A dialog popup for the new server data.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'login_dialog_base.ui'))


class NewServerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

    def values(self):
        values_dic = {
            'name': self.name.text(),
            'url': self.url.text(),
        }
        return values_dic