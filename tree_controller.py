# -*- coding: utf-8 -*-
"""
This script contains the class TreeController: controlls the behavior of the
items in the dock tree.
"""

from .project_item import ProjectItem


class TreeController:
    def __init__(self, tree):
        self.tree = tree

        def double_clicked(item):
            if isinstance(item, ProjectItem):
                item.double_clicked()

        tree.itemDoubleClicked.connect(double_clicked)
