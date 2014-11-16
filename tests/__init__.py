from unittest import TestCase

from srtime.process import Process

class TestProcess(TestCase):
    def test_tmpfile_is_string(self):
        t = Process._get_tmpfile()
        self.assertTrue(isinstance(t, str))
