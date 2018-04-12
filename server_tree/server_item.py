# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMenu, QAction, QTreeWidgetItem, QPushButton

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

        def close():
            self.delete()
        close_action = QAction('&Close connection')
        menu.addAction(close_action)
        close_action.triggered.connect(close)

        menu.exec_(pos)

    def _expanded(self):
        if self.childCount() == 1 and isinstance(self.child(0), LoadingItem):
            if not self.giscube.is_logged_in:
                if not self._login_popup():
                    return

            main_company.list_job(ListProjectsJob(self))

    def _login_popup(self):
        while True:
            dialog = LoginDialog(self.treeWidget())
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
            except Exception as e:
                print(e)  # TODO actually do something

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
        self.succeded = False

    def do_work(self):
        """
        Do the asynchronous job.
        Reuests the server the list of projects.
        """
        try:
            self.projects = self.si.giscube.qgis_server.projects()
            self.succeded = True
        except Unauthorized:
            pass  # TODO do message?

    def apply_result(self):
        """
        Apply the results after the asynchronous job has been done.
        Updates the GUI.
        """
        if self.succeded:
            self.si.takeChildren()
            for pid, name in self.projects.items():
                ProjectItem(pid, name, self.si)
        elif self.si._login_popup():
            main_company.list_job(self)
