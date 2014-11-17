from unittest import TestCase

from srtime.process import Process

class TestProcess(TestCase):
    def test_times_list(self):
        times = Process({}).times()
        self.assertTrue(isinstance(times, list))
        self.assertTrue(len(times) == 0)
