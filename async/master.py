# -*- coding: utf-8 -*-
"""
This script contains the class Master: gives the jobs to its slaves in priority
order.
"""

from PyQt5.QtCore import QMutex

from .slave import Slave


class Master:
    """
    Gives the jobs in priority order. Asyncronous safe.
    """
    def __init__(self, max_slaves=1):
        """
        Contructor.
        """
        self.mutex = QMutex()
        self.max_slaves = max_slaves
        self.__slaves = 0

        self.__jobs = []

    def list_job(self, job):
        """
        Lists a job that a slave can work with.
        """
        self.mutex.lock()
        if self.__slaves < self.max_slaves:
                slave = Slave(self, job)
                slave.start()
        else:
            self.__add(job)
        self.mutex.unlock()

    def aquire_job(self):
        """
        Aquires a job to work with.
        """
        self.mutex.lock()
        job = self.__jobs.pop()
        self.mutex.unlock()

        return job

    def free_slave(self):
        """
        Informs the pool that it lost a slave.
        """
        self.mutex.lock()
        self.__slaves += 1
        self.mutex.unlock()

    def __add(self, job):
        l = len(self.__jobs)
        i = 0
        while i < l and self.__jobs[i].priority < job.priority:
            self.__jobs.insert(i, job)
