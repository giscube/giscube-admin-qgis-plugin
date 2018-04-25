# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from requests.exceptions import RequestException

from PyQt5.QtCore import QSettings, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMenu, QAction, QTreeWidgetItem, QPushButton

from qgis.gui import QgsMessageBar

from ..settings import Settings

from ..async import Job
from ..main_company import main_company

from ..backend import Unauthorized

from .loading_item import LoadingItem
from .project_item import ProjectItem
from .login_dialog import LoginDialog


class ServerItem(QTreeWidgetItem):
    """
    Server instance on the plugin's server tree UI.
    Controlls and keeps the information of the connection to the server and
    handles the interaction with the user.
    """
    saved_servers = QSettings(
        Settings.ORGANIZATION,
        Settings.PROJECT + '-servers',
    )

    def __init__(self, conn, tree, giscube_admin):
        """
        Contructor.
        :param conn: The connection to the server.
        :type  conn: ..backend.Giscube
        :param tree: Widget that will contain this object.
        :type  tree: PyQt5.QtWidgets.QTreeWidget
        :param giscube_admin: Main plugin's object.
        :type  giscube_admin: GiscubeAdmin
        """
        super().__init__()

        self.giscube_admin = giscube_admin
        self.iface = giscube_admin.iface
        self.giscube = conn
        self._tree = tree

        tree.addTopLevelItem(self)

        self.setText(0, self.name)

        self.new_project = QPushButton('New Project')
        tree.setItemWidget(self, 1, self.new_project)
        self.new_project.clicked.connect(
            lambda: self.giscube_admin.new_project_popup(self.name)
            )

        key = self.name+'/url'
        if not self.saved_servers.contains(key):
            self.saved_servers.setValue(key, self.giscube.server_url)
            self.saved_servers.sync()

        self.addChild(LoadingItem())

    @property
    def name(self):
        """
        Name of the server.
        """
        return self.giscube.name

    @property
    def server_url(self):
        return self.giscube.server_url

    def delete(self):
        # Remove tokens and prevent saving them again
        self.giscube.save_tokens = False

        # Remove from configuration file
        key = self.name+'/url'
        if self.saved_servers.contains(key):
            self.saved_servers.remove(key)
            self.saved_servers.sync()

        # Apply to GUI
        index = self._tree.indexOfTopLevelItem(self)
        self._tree.takeTopLevelItem(index)

    def context_menu(self, pos):
        menu = QMenu()

        def refresh():
            main_company.list_job(ListProjectsJob(self))
        refresh_action = QAction('&Refresh projects')
        menu.addAction(refresh_action)
        refresh_action.triggered.connect(refresh)

        def admin_webside():
            QDesktopServices.openUrl(QUrl(self.giscube.admin_webside))
        admin_webside_action = QAction('&Open admin webside')
        menu.addAction(admin_webside_action)
        admin_webside_action.triggered.connect(admin_webside)

        def close():
            self.delete()
        close_action = QAction('Remove server')
        menu.addAction(close_action)
        close_action.triggered.connect(close)

        menu.exec_(pos)

    def _expanded(self):
        if isinstance(self.child(0), LoadingItem):
            if not self.giscube.is_logged_in:
                if not self._login_popup():
                    return
            main_company.list_job(ListProjectsJob(self))

    def _login_popup(self):
        dialog = LoginDialog(self.treeWidget())
        while True:
            if not dialog.exec_():
                self._tree.collapseItem(self)
                return False

            result = dialog.values()
            self.giscube.save_tokens = False
            try:
                if self.giscube.login(
                        result['username'],
                        result['password']):
                    self.giscube.save_tokens = result['save_tokens']
                    break
                else:
                    dialog.error.setText("Incorrect username or password.")
            except RequestException as e:
                self.iface.messageBar().pushMessage(
                    "Error",
                    "No s'ha pogut connectar al servidor",
                    QgsMessageBar.ERROR
                )

        return True


class ListProjectsJob(Job):
    """
    Lists the projects of a ServerItem asynchronously.
    """
    def __init__(self, si):
        """
        Contructor.
        """
        super().__init__()
        self.si = si
        self.projects = None
        self.services = None
        self.succeded = False

    def do_work(self):
        """
        Do the asynchronous job.
        Reuests the server the list of projects.
        """
        qgis_server = self.si.giscube.qgis_server
        self.projects, self.services = qgis_server.projects()
        self.succeded = True

    def apply_result(self):
        """
        Apply the results after the asynchronous job has been done.
        Updates the GUI.
        """
        if self.succeded:
            self.si.takeChildren()
            for pid, name in self.projects.items():
                if pid in self.services:
                    service = self.services[pid]
                else:
                    service = None

                ProjectItem(pid, name, self.si, service)
        elif self.si._login_popup():
            main_company.list_job(self)

    def exception_risen(self, exception):
        try:
            super().exception_risen(exception)
        except Unauthorized:
            # The saved credential expired. Remove them and start the loging
            #   and querying again.
            self.si.giscube.delete_saved()
            self.si._expanded()
        except RequestException as e:
            self.iface.messageBar().pushMessage(
                "Error",
                "No s'ha pogut connectar al servidor",
                QgsMessageBar.ERROR
            )
