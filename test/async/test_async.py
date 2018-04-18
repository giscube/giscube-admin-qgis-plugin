# -*- coding: utf-8 -*-
"""
This script tests the async package.
"""

import time
from unittest import TestCase

from async import Company
from .append_job import AppendJob
from .sleep_job import SleepJob


class TestAsync(TestCase):
    def test_job(self):
        company = Company(max_slaves=1)

        company.list_job(SleepJob(t=1))

        l = []
        company.list_job(AppendJob(l, 'hello'))

        time.sleep(3)

        self.assertEqual(len(l), 1)
