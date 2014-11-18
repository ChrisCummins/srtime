from unittest import TestCase, main

import srtime
from srtime.process import Process

class TestProcess(TestCase):


    def test_times_list(self):
        times = Process({}).times()
        self.assertTrue(isinstance(times, list))
        self.assertTrue(len(times) == 0)


if __name__ == '__main__':
    main()
