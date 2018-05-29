# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from requests.exceptions import RequestException

from PyQt5.QtCore import QSettings, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMenu, QAction, QTreeWidgetItem, QMessageBox

from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ..settings import Settings

from ..backend import Unauthorized

from ..async import Job
from ..main_company import main_company

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
        """
        Base URL to the server.
        """
        return self.giscube.server_url

    def delete(self):
        """
        Remove this server instance and its data (including the saved) and
        update the UI.
        """
        # Remove tokens and prevent saving them again
        self.giscube.remove_tokens()

        # Remove from configuration file
        key = self.name+'/url'
        if self.saved_servers.contains(key):
            self.saved_servers.remove(key)
            self.saved_servers.sync()

        # Apply to GUI
        index = self._tree.indexOfTopLevelItem(self)
        self._tree.takeTopLevelItem(index)

    def refresh_projects(self):
        main_company.list_job(ListProjectsJob(self))

    def new_project_dialog(self):
        self.giscube_admin.new_project_popup(self.name)

    def context_menu(self, pos):
        menu = QMenu()

        def logout():
            self.giscube.remove_tokens()
            self.setExpanded(False)
            self.takeChildren()
            self.addChild(LoadingItem())
        logout_action = QAction('Logout from server')
        menu.addAction(logout_action)
        logout_action.triggered.connect(logout)

        def admin_webside():
            QDesktopServices.openUrl(QUrl(self.giscube.admin_webside))
        admin_webside_action = QAction('Open admin webside')
        menu.addAction(admin_webside_action)
        admin_webside_action.triggered.connect(admin_webside)

        def close():
            confirm_dialog = QMessageBox(
                QMessageBox.Question,
                "Confirm server removal",
                "Do you really want to remove this server?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm_dialog.exec_() == QMessageBox.Yes:
                self.delete()
        close_action = QAction('Remove server')
        menu.addAction(close_action)
        close_action.triggered.connect(close)

        menu.exec_(pos)

    def _expanded(self):
        if isinstance(self.child(0), LoadingItem):
            if not self.giscube.is_logged_in:
                if not self._login_popup():
                    self.setExpanded(False)
                    return
            main_company.list_job(ListProjectsJob(self))

    def _try_login(self, username, password, save_tokens):
        try:
            if self.giscube.login(username, password):
                self.giscube.save_tokens = save_tokens
                return {'finished': True, 'correct': True}
        except RequestException as e:
            self.iface.messageBar().pushMessage(
                "Error",
                "Unable to connect to the server",
                Qgis.Critical
            )
            self.giscube.save_tokens = False
            return {'finished': True, 'correct': False}
        return {'finished': False, 'correct': False}

    def _login_popup(self, retry=False):
        dialog = LoginDialog(self._tree)
        status = {'finished': False, 'correct': not retry}
        while not status['finished']:
            if not status['correct']:
                dialog.error.setText("Incorrect username or password.")
            if not dialog.exec_():
                self._tree.collapseItem(self)
                return False
            result = dialog.values()
            status = self._try_login(
                result['username'],
                result['password'],
                result['save_tokens'],
                )
        return status['correct']


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
        """
        Handle the exception if anything goes wrong.
        """
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
