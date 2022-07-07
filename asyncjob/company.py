# -*- coding: utf-8 -*-
"""
This script contains the class Company: manages the slaves and the available
jobs.
"""

from PyQt5.QtCore import QMutex

from .slave import Slave


class Company:
    """
    Manages the creation Slaves as well as gives them the Jobs to work on.
    """
    def __init__(self, max_slaves=1):
        """
        Contructor.
        :param max_slaves: The maximum number of slaves (working threads)
        desired.
        :type max_slaves:  int
        """
        self._max_slaves = max_slaves
        self._slaves = []
        self._free_slaves = []

        self._jobs = []

        self._mutex = QMutex()
        self._free_mutex = QMutex()

    @property
    def max_slaves(self):
        """
        The maximum number of slaves (working threads) that may be used.
        """
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
        Lists a job. An Slave will work on it at when no higher priority jobs
        are left (if two jobs have the same priority, the frist listed is
        executed first).
        :param job: Job that contains the work to be done.
        :type job:  .async.Job
        """
        self._mutex.lock()
        if len(self._slaves) < self._max_slaves:
                slave = Slave(self, job)
                self._slaves.append(slave)
                slave.start()
        else:
            self.__add(job)
        self._mutex.unlock()

    def _aquire_job(self, slave):
        """
        Aquire a job for an slave.
        :param slave: Slave that will do the job.
        :type slave:  .async.Slave
        """
        self._mutex.lock()
        if len(self._jobs) > 0:
            job = self._jobs.pop()
        else:
            job = None

            # The slave will be free after this (no more jobs to be done).
            # We can no longer use it but we have to keep an instance until
            #  it is free to prevent the garbage collector to destroy it too
            #  soon. So we move it to another list.
            for i, s in enumerate(self._slaves):
                if s is slave:
                    self._slaves.pop(i)

                    self._free_mutex.lock()
                    self._free_slaves.append(slave)
                    self._free_mutex.unlock()
        self._mutex.unlock()

        return job

    def free_slave(self, slave):
        """
        Frees a slave. Removes the last instance of the thread.
        :param slave: Slave to be freed.
        :type slave:  .async.Slave
        """
        if type(slave) is not Slave:
            raise TypeError("The argument slave must be of type"
                            ".async.Slave")

        self._free_mutex.lock()
        for i, s in enumerate(self._free_slaves):
            if s is slave:
                self._free_slaves.pop(i)
        self._free_mutex.unlock()

    def __add(self, job):
        # Call with self._mutex locked
        l = len(self._jobs)
        i = 0
        while i < l and self._jobs[i].priority < job.priority:
            i += 1

        self._jobs.insert(i, job)
