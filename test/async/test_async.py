# -*- coding: utf-8 -*-
"""
This script tests the async package.
"""

import time
from unittest import TestCase

from async import Master
from .append_job import AppendJob
from .sleep_job import SleepJob


class TestAsync(TestCase):
    def test_job(self):
        master = Master(max_slaves=1)

        master.list_job(SleepJob(t=1))

        l = []
        master.list_job(AppendJob(l, 'hello'))

        time.sleep(3)

        self.assertEqual(len(l), 1)
