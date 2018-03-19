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

    def work(self):
        """
        Does the job itself. Override to make a job do something.
        """
        pass

    def apply(self):
        """
        After the job is done, apply the result in the main thread.
        Normally used to update GUI.
        """
        pass
