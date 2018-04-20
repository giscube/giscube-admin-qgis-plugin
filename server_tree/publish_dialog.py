# -*- coding: utf-8 -*-
"""
This script contains NewServerDialog.
"""

import os

from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'publish_dialog_base.ui'))


class PublishDialog(QtWidgets.QDialog, FORM_CLASS):
    """
    Popup dialog that ask for the necessary data to publish a project.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

    def values(self):
        values_dic = {
            'title': self.title.text(),
            'description': self.descr.toPlainText(),
            'keywords': self.keywords.text(),
            'visible_on_geoportal': self.visible_on_geoportal.isChecked(),
        }
        return values_dic
