# -*- coding: utf-8 -*-
"""
This script contains ServerItem: The instance of the server UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton

from ..async import Job
from ..main_company import main_company

from ..backend import Unauthorized

from .loading_item import LoadingItem
from .project_item import ProjectItem

from .login_dialog import LoginDialog


class ServerItem(QTreeWidgetItem):
    def __init__(self, conn, tree):
        super().__init__()

        self.giscube = conn
        self._tree = tree

        tree.addTopLevelItem(self)

        self.setText(0, self.name)

        self.new_project = QPushButton('New Project')
        tree.setItemWidget(self, 1, self.new_project)

        self.addChild(LoadingItem())

    @property
    def name(self):
        return self.giscube.name

    @property
    def server_url(self):
        self.giscube.server_url

    @property
    def save_tokens(self):
        self.giscube.save_tokens

    def expanded(self):
        if self.childCount() == 1 and isinstance(self.child(0), LoadingItem):
            if not self.giscube.is_logged_in:
                self._login_popup()

            main_company.list_job(ListProjectsJob(self))

    def _login_popup(self):
        while True:
            dialog = LoginDialog(self.treeWidget())
            if not dialog.exec_():
                self._tree.collapseItem(self)
                return

            result = dialog.values()
            self.giscube.save_tokens = False
            try:
                if self.giscube.login(
                        result['username'],
                        result['password']):
                    self.giscube.save_tokens = result['save_tokens']
                    break
            except:
                pass  # TODO Detect error and show message


class ListProjectsJob(Job):
    def __init__(self, si):
        super().__init__()
        self.si = si
        self.projects = None
        self.succeded = False

    def do_work(self):
        try:
            self.projects = self.si.giscube.qgis_server.projects()
            self.succeded = True
        except Unauthorized:
            pass  # TODO do message?

    def apply_result(self):
        if self.succeded:
            self.si.takeChildren()
            for pid, name in self.projects.items():
                ProjectItem(pid, name, self.si)
        else:
            self.si._login_popup()
            main_company.list_job(self)
