# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GiscubeAdminDockWidget
                                 A QGIS plugin
 A graphical Giscube administration tool
                             -------------------
        begin                : 2018-02-15
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Martí Angelats i Ribera
        email                : marti.angelats@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_dockwidget_base.ui'))


class GiscubeAdminDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(GiscubeAdminDockWidget, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Add signals and slots connections
        self.loginSubmit.clicked.connect(self.__login)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def __login(self):
        pass # TODO actual login
