# -*- coding: utf-8 -*-
"""
This script contains the class Job: action to be done.
"""


class Job:
    """
    Represents a job to be done.
    """
    def __init__(self, priority=0.0):
        """
        Contructor.
        :param priority: Priority of the job.
        :type priority: float
        """
        self.priority = priority

    def work(self, worker):
        """
        Does the job itself. Override to make a job do something.
        """
        pass
