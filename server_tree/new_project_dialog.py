"""
This script contains NewServerDialog.
"""

import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from qgis.core import QgsProject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'new_project_dialog_base.ui'))


class NewProjectDialog(QtWidgets.QDialog, FORM_CLASS):
    """
    Popup dialog that ask for the necessary data to make a new server
    connection.
    """
    def __init__(self, giscube_admin, server=None, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        self.giscube_admin = giscube_admin

        server_names = giscube_admin.server_names()

        # Add all the servers to the lsit and select ours
        self.servers.clear()
        self.servers.addItems(server_names)

        try:
            index = server_names.index(server)
        except ValueError:
            index = 0
        self.servers.setCurrentIndex(index)

        self.name.setText('New Project')

        self.current.clicked.connect(lambda: self._add_current_project())
        self.blank.clicked.connect(lambda: self._add_blank_project())
        self.file.clicked.connect(lambda: self._add_file_project())

    def _add_current_project(self):
        self.accept()

    def _add_blank_project(self):
        self.giscube_admin.iface.newProjectCreated.connect(
            lambda: self._add_current_project(),
            Qt.DirectConnection)
        self.giscube_admin.iface.newProject(True)

    def _add_file_project(self):
        def open_project():
            self.giscube_admin.iface.newProjectCreated.disconnect(
                open_project)
            project = QgsProject.instance()
            path = dialog.selectedFiles()[0]
            project.read(path)
            self._add_current_project()

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("QGIS project (*.qgs)")
        if dialog.exec_():
            self.giscube_admin.iface.newProjectCreated.connect(
                open_project,
                Qt.DirectConnection)
            self.giscube_admin.iface.newProject(True)
