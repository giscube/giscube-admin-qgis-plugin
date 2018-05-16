# -*- coding: utf-8 -*-
"""
This script contains the class TreeController.
"""

from .server_item import ServerItem
from .project_item import ProjectItem


class TreeController:
    """
    Forwards the desired signals to the correct item in the tree.
    """
    def __init__(self, tree):
        self.tree = tree

        def context_menu(pos):
            item = self.tree.itemAt(pos)
            if item is not None:
                vp = self.tree.viewport()
                global_pos = vp.mapToGlobal(pos)
                item.context_menu(global_pos)
        tree.customContextMenuRequested.connect(context_menu)

        def expanded(item):
            if isinstance(item, ServerItem):
                item._expanded()
        tree.itemExpanded.connect(expanded)

        def double_clicked(item):
            if isinstance(item, ProjectItem):
                item._double_clicked()
        tree.itemDoubleClicked.connect(double_clicked)
