# -*- coding: utf-8 -*-
"""
This script contains the class Slave: it the jobs on the list in its own
thread.
"""

from PyQt5.QtCore import Qt, pyqtSignal, QThread
from .job import Job


class Slave(QThread):
    """
    Performs jobs. It's its own thread.
    """
    job_done = pyqtSignal(Job)

    def __init__(self, master, job):
        super(Slave, self).__init__()
        self.master = master
        self.job = job

        def apply_job(j):
            j.apply()
        self.job_done.connect(apply_job, Qt.QueuedConnection)

        self.finished.connect(lambda: master.free_slave(self))

    def run(self):
        """
        Start working.
        """
        if self.job is None:
            return

        while True:
            self.job.work()
            self.job_done.emit(self.job)

            self.job = self.master.aquire_job(self)
            if self.job is None:
                return
