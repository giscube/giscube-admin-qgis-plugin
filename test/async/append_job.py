# -*- coding: utf-8 -*-
"""
This script contains a Job class for testing the async package.
"""
import time

from asyncjob import Job


class AppendJob(Job):
    def __init__(self, l, value):
        super(AppendJob, self).__init__()
        self.list = l
        self.value = value

    def do_work(self):
        time.sleep(1)
        self.list.append(self.value)
