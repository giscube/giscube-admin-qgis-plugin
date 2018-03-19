# -*- coding: utf-8 -*-
"""
This script contains Server: The instance of the server UI.
"""

from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton

from .async import Job
from .project_item import ProjectItem


class ServerItem(QTreeWidgetItem):
    def __init__(self, name, conn, root, company):
        super(ServerItem, self).__init__()

        self.company = company
        self.name = name
        self.giscube_conn = conn
        self.root = root

    def setupUI(self):
        self.setText(0, self.name)

        self.new_project = QPushButton('New Project')
        self.root.setItemWidget(self, 1, self.new_project)

        self.company.list_job(SetupProjectsJob(self))


class SetupProjectsJob(Job):
    def __init__(self, si):
        super(SetupProjectsJob, self).__init__()
        self.si = si
        self.projects = None

    def work(self):
        self.projects = self.si.giscube_conn.qgis_server.projects()

    def apply(self):
        for pid, name in self.projects.items():
            project = ProjectItem(pid, name, self.si.root)
            self.si.addChild(project)
            project.setupUI()
