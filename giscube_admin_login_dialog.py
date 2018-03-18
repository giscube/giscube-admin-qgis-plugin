# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdminLoginDialog: A dialog that asks the user for
the logging credentials.
"""

import os
from requests.exceptions import ConnectionError

from PyQt5 import QtWidgets, uic

from .backend import Giscube
from .backend.utils import is_url_valid

from .server_item import ServerItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'giscube_admin_login_dialog_base.ui'))


class GiscubeAdminLoginDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, giscube_admin, parent=None):
        """Constructor."""
        super(GiscubeAdminLoginDialog, self).__init__(parent)

        self.giscube_admin = giscube_admin
        self.client_id = giscube_admin.CLIENT_ID

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Connect to validation
        self.login.clicked.connect(self.__validate)

    def __validate(self):
        self.error.setText('')

        name = self.name.text()
        if name in self.giscube_admin.server_names():
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

        conn = Giscube(
            url,
            self.client_id,
            name=name,
            save_tokens=self.giscube_admin.settings.save_connections)

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

        server = ServerItem(name, conn, self.giscube_admin.servers)
        self.giscube_admin.servers.addTopLevelItem(server)
        server.setupUI()

        self.accept()
