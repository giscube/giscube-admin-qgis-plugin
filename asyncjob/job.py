# -*- coding: utf-8 -*-
"""
This script contains the class Job.
"""


class Job:
    """
    Represents a job to be done. Override this class to do your own job.
    """
    def __init__(self, priority=0.0):
        """
        Contructor.
        :param priority: Priority of the job.
        :type priority:  float
        """
        self.priority = priority

    def do_work(self):
        """
        Do the asynchronous job.
        """
        pass

    def apply_result(self):
        """
        Apply the results after the asynchronous job has been done.
        Normally used to update GUI.
        """
        pass

    def exception_risen(self, exception):
        """
        There was an error during the asynchronous execution.
        """
        raise exception
