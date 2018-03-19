# -*- coding: utf-8 -*-
"""
This script contains the class Slave: it the jobs on the list in its own
thread.
"""

from PyQt5.QtCore import QThread


class Slave(QThread):
    """
    Performs jobs. It's its own thread.
    """
    def __init__(self, pool, job):
        super(Slave, self).__init__()
        self.pool = pool
        self.job = job

    def run(self):
        """
        Start working.
        """
        if self.job is None:
            self.pool.free_worker()

        while True:
            self.job.work()

            self.job = self.pool.aquire_job()
            if self.job is None:
                break

        self.pool.free_worker()
