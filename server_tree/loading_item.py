# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem


class LoadingItem(QTreeWidgetItem):
    def __init__(self):
        super().__init__()

        self.setText(0, 'Loading...')
