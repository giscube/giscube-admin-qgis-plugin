# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminLoginDialog: A dialog that asks the user for
the logging credentials.
"""

import os

from PyQt5 import QtWidgets, uic

from .backend import Giscube
from .backend.utils import is_url_valid

from requests.exceptions import ConnectionError

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_login_dialog_base.ui'))


class GiscubeAdminLoginDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, giscube_admin, parent=None):
        """Constructor."""
        super(GiscubeAdminLoginDialog, self).__init__(parent)

        self.conns = giscube_admin.conns
        self.client_id = giscube_admin.CLIENT_ID

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Connect to validation
        self.login.clicked.connect(self.__validate)

    def __validate(self):
        self.error.setText('')

        name = self.name.text()
        if name in self.conns:
            self.error.setText('There already is a server with this name. '
                               'Please, choose another one.')
            return

        url = self.url.text()
        if not is_url_valid(url, ('http', 'https')):
            self.error.setText('Invalid server URL. '
                               'Please, choose another one.')
            return

        username = self.username.text()
        password = self.password.text()

        conn = Giscube(url, self.client_id, name=name, save_tokens=False)
        try:
            if not conn.login(username, password):
                self.error.setText('Wrong credentials or server URL. '
                                   'Please, try again.')
                return
        except ConnectionError:
            self.error.setText('Couldn\'t connect to the server. '
                               'Please, check the URL and the connection.')
            return
        except Exception as e:
            self.error.setText('An error was rised when trying to connect to '
                               'the server.\n'
                               'Full exception: ' + str(e))
            return

        self.conns[name] = conn
        self.accept()
