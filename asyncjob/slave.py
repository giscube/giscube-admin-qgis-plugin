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
    _job_done = pyqtSignal(Job)
    _exception_risen = pyqtSignal(Job, Exception)

    def __init__(self, company, job):
        """
        Constructor.
        :param company: The company that gives the jobs to be made.
        :type company:  .async.Company
        :param job: An inital job to be done.
        :type job:  .async.Job
        """

        super(Slave, self).__init__()
        self.company = company
        self.job = job

        def apply_job_result(j):
            j.apply_result()
        self._job_done.connect(apply_job_result, Qt.QueuedConnection)

        def exception_risen(j, e):
            j.exception_risen(e)
        self._exception_risen.connect(exception_risen, Qt.QueuedConnection)

        self.finished.connect(lambda: company.free_slave(self))

    def run(self):
        """
        Start working.
        """
        if self.job is None:
            return

        while True:
            try:
                self.job.do_work()
                self._job_done.emit(self.job)
            except Exception as e:
                self._exception_risen.emit(self.job, e)

            self.job = self.company._aquire_job(self)
            if self.job is None:
                return
