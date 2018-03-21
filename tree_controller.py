# -*- coding: utf-8 -*-
"""
This script contains the class TreeController: controlls the behavior of the
items in the dock tree.
"""

from .server_tree.server_item import ServerItem
from .server_tree.project_item import ProjectItem


class TreeController:
    def __init__(self, tree):
        self.tree = tree

        def expanded(item):
            if isinstance(item, ServerItem):
                item.expanded()
        tree.itemExpanded.connect(expanded)

        def double_clicked(item):
            if isinstance(item, ProjectItem):
                item.double_clicked()
        tree.itemDoubleClicked.connect(double_clicked)
