# -*- coding: utf-8 -*-
"""
This script contains the class Slave: it the jobs on the list in its own
thread.
"""

from PyQt5.QtCore import Qt, pyqtSignal, QThread

from .company import Company
from .job import Job


class Slave(QThread):
    """
    Performs jobs. It's its own thread.
    """
    _job_done = pyqtSignal(Job)

    def __init__(self, company, job):
        """
        Constructor.
        :param company: The company that gives the jobs to be made.
        :type company:  .async.Company
        :param job: An inital job to be done.
        :type job:  .async.Job
        """
        if type(company) is not Company:
            raise TypeError("The argument company must be of type"
                            ".async.Company")
        if type(job) is not Job:
            raise TypeError("The argument company must be of type"
                            ".async.Job")

        super(Slave, self).__init__()
        self.company = company
        self.job = job

        def apply_job_result(j):
            j.apply_result()
        self._job_done.connect(apply_job_result, Qt.QueuedConnection)

        self.finished.connect(lambda: company.free_slave(self))

    def run(self):
        """
        Start working.
        """
        if self.job is None:
            return

        while True:
            self.job.do_work()
            self._job_done.emit(self.job)

            self.job = self.company.aquire_job(self)
            if self.job is None:
                return
