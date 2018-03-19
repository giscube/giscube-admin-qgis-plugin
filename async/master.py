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
        self.__slaves = []
        self.__free_slaves = []
        self.free_mutex = QMutex()

        self.__jobs = []

    def list_job(self, job):
        """
        Lists a job that a slave can work with.
        """
        self.mutex.lock()
        if len(self.__slaves) < self.max_slaves:
                slave = Slave(self, job)
                self.__slaves.append(slave)
                slave.start()
        else:
            self.__add(job)
        self.mutex.unlock()

    def aquire_job(self, slave):
        """
        Aquires a job to work with.
        """
        self.mutex.lock()
        if len(self.__jobs) > 0:
            job = self.__jobs.pop()
        else:
            job = None
            for i, s in enumerate(self.__slaves):
                if s is slave:
                    self.free_mutex.lock()
                    self.__free_slaves.append(self.__slaves.pop(i))
                    self.free_mutex.unlock()
        self.mutex.unlock()

        return job

    def free_slave(self, slave):
        """
        Informs the pool that it lost a slave.
        """
        self.free_mutex.lock()
        for i, s in enumerate(self.__free_slaves):
            if s is slave:
                self.__free_slaves.pop(i)
        self.free_mutex.unlock()

    def __add(self, job):
        l = len(self.__jobs)
        i = 0
        while i < l and self.__jobs[i].priority < job.priority:
            i += 1

        self.__jobs.insert(i, job)
