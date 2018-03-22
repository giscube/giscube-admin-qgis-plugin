# -*- coding: utf-8 -*-
"""
This script contains ServerItem.
"""

from PyQt5.QtWidgets import QTreeWidgetItem


class LoadingItem(QTreeWidgetItem):
    """
    Simple placeholder tree item that says 'Loading...'.
    """
    def __init__(self):
        super().__init__()

        self.setText(0, 'Loading...')
