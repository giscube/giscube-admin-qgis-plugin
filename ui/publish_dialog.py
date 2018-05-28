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
    Popup dialog to make or edit a project's publication.
    """
    def __init__(self, project_item, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        self.project_item = project_item
        self.categories = {}
        self.categories_inv = {"": None}

        name = project_item.name
        published = project_item.published

        self.title.setText(published.get('title', name))
        self.descr.setPlainText(published.get('description'))
        self.keywords.setText(published.get('keywords'))
        self.visible_on_geoportal.setChecked(
            published.get('visible_on_geoportal', True)
        )

        self.__category_setup(published.get('category'))

    def values(self):
        """
        Returns a dictionary with the values of this dialog's widgets.
        """
        values_dic = {
            'title': self.title.text(),
            'description': self.descr.toPlainText(),
            'keywords': self.keywords.text(),
            'on_geoportal': self.visible_on_geoportal.isChecked(),
            'category': self.__get_category()
        }
        return values_dic

    def __category_setup(self, current=None):
        category_api = self.project_item.server_item.giscube.category_api
        categories = category_api.get_categories()
        self.categories = {}
        self.categories_inv = {"": None}

        selected = ""

        for id, category in categories.items():
            name = category.name
            while category.parent is not None:
                p = categories[category.parent]
                name = p.name + " > " + name
                category = p
            self.categories[id] = name
            self.categories_inv[name] = id
            if current is not None and current == id:
                selected = name

        self.category.addItems(sorted(self.categories_inv.keys()))
        self.category.setCurrentIndex(self.category.findText(selected))

    def __get_category(self):
        return self.categories_inv[self.category.currentText()]
