# -*- coding: utf-8 -*-
"""
This script contains a Job class for testing the async package.
"""

import time

from async import Job


class SleepJob(Job):
    def __init__(self, t=3):
        super(SleepJob, self).__init__()
        self.t = t

    def do_work(self):
        time.sleep(self.t)
