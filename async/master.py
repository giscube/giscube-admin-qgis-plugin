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
        self._max_slaves = max_slaves
        self._slaves = []
        self._free_slaves = []

        self._jobs = []

        self._mutex = QMutex()
        self._free_mutex = QMutex()

    @property
    def max_slaves(self):
        self._mutex.lock()
        r = self.__max_slaves
        self._mutex.unlock()

        return r

    @max_slaves.setter
    def max_slaves(self, v):
        self._mutex.lock()
        self.__max_slaves = v
        self._mutex.unlock()

    def list_job(self, job):
        """
        Lists a job that a slave can work with.
        """
        self._mutex.lock()
        if len(self._slaves) < self._max_slaves:
                slave = Slave(self, job)
                self._slaves.append(slave)
                slave.start()
        else:
            self.__add(job)
        self._mutex.unlock()

    def aquire_job(self, slave):
        """
        Aquires a job to work with.
        """
        self._mutex.lock()
        if len(self._jobs) > 0:
            job = self._jobs.pop()
            self._mutex.unlock()
        else:
            job = None

            # The slave will be free after this (no more jobs to be done).
            # We can no longer use it but we have to keep an instance until
            #  it is free to prevent the garbage collector to destroy it too
            #  soon. So we move it to another list.
            for i, s in enumerate(self._slaves):
                if s is slave:
                    self._slaves.pop(i)
                    self._mutex.unlock()

                    self._free_mutex.lock()
                    self._free_slaves.append(slave)
                    self._free_mutex.unlock()

        return job

    def free_slave(self, slave):
        """
        Informs the pool that it lost a slave.
        """
        self._free_mutex.lock()
        for i, s in enumerate(self._free_slaves):
            if s is slave:
                self._free_slaves.pop(i)
        self._free_mutex.unlock()

    def __add(self, job):
        l = len(self._jobs)
        i = 0
        while i < l and self._jobs[i].priority < job.priority:
            i += 1

        self._jobs.insert(i, job)